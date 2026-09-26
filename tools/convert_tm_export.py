"""Convert a genuine float32 TFJS layers export, without training new weights.

Uses tf-keras legacy deserialization and TensorFlow's TFLite converter.
The limited weight decoder intentionally rejects quantized/unsupported exports.
Reference: tensorflow/tfjs keras_tfjs_loader.py and Teachable Machine converter.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
os.environ.setdefault('TF_USE_LEGACY_KERAS', '1')
import numpy as np
import tensorflow as tf
import tf_keras
from PIL import Image, ImageOps

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('experiment', type=Path)
    args=parser.parse_args()
    src=args.experiment/'tfjs'
    dst=args.experiment/'tflite'
    config=json.loads((src/'model.json').read_text())
    metadata=json.loads((src/'metadata.json').read_text())
    model=tf_keras.models.model_from_json(json.dumps(config['modelTopology']))
    decoded={}
    for group in config['weightsManifest']:
        raw=b''.join((src/name).read_bytes() for name in group['paths'])
        offset=0
        for weight in group['weights']:
            if weight['dtype']!='float32' or 'quantization' in weight:
                raise ValueError('Only unquantized float32 exports are supported')
            count=int(np.prod(weight['shape']))
            decoded[weight['name']]=np.frombuffer(raw,dtype='<f4',count=count,offset=offset).reshape(weight['shape']).copy()
            offset+=count*4
        if offset!=len(raw):
            raise ValueError('Weight byte length mismatch')
    names=[w.name.split(':')[0] for w in model.weights]
    if set(names)!=set(decoded) or len(names)!=len(decoded):
        raise ValueError(f'Weight name mismatch: {set(names)^set(decoded)}')
    model.set_weights([decoded[name] for name in names])
    dst.mkdir(parents=True,exist_ok=True)
    converter=tf.lite.TFLiteConverter.from_keras_model(model)
    tflite=converter.convert()
    (dst/'model_unquant.tflite').write_bytes(tflite)
    (dst/'labels.txt').write_text(''.join(f'{i} {label}\n' for i,label in enumerate(metadata['labels'])),encoding='utf-8')
    interpreter=tf.lite.Interpreter(model_content=tflite)
    interpreter.allocate_tensors()
    inp=interpreter.get_input_details()[0]
    out=interpreter.get_output_details()[0]
    root=Path(__file__).resolve().parents[1]
    checks=[]
    for label in metadata['labels']:
        path=next((root/'dataset_public'/'train_e1'/label).glob('*.jpg'))
        with Image.open(path) as image:
            image=ImageOps.fit(ImageOps.exif_transpose(image).convert('RGB'),(224,224),method=Image.Resampling.LANCZOS)
            x=np.expand_dims(np.asarray(image,dtype=np.float32)/127.5-1,0)
        expected=model(x,training=False).numpy()
        interpreter.set_tensor(inp['index'],x)
        interpreter.invoke()
        actual=interpreter.get_tensor(out['index'])
        difference=float(np.max(np.abs(expected-actual)))
        if difference>.0001 or int(expected.argmax())!=int(actual.argmax()):
            raise ValueError('Keras/TFLite parity failed')
        checks.append({'image':str(path.relative_to(root)),'max_abs_difference':difference,'keras':expected.tolist(),'tflite':actual.tolist()})
    report={'method':'Local format conversion of Teachable Machine TFJS export; no retraining',
            'tensorflow':tf.__version__,'tf_keras':tf_keras.__version__,'weights_loaded':len(names),
            'tflite_sha256':hashlib.sha256(tflite).hexdigest(),'parity_checks':checks,
            'limitation':'Keras/TFLite numeric parity on 3 training images only, not external accuracy or independent TFJS parity'}
    (args.experiment/'conversion.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
    main()
