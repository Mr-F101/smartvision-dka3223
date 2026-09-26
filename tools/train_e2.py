"""Train Experiment 2 (E2) using MobileNetV2 base from E1 and export to TFJS & TFLite.

E1: 50 epochs, batch size 16, lr 0.001 (baseline)
E2: 100 epochs, batch size 16, lr 0.001 (increased epochs for convergence study)
"""
import os
os.environ.setdefault('TF_USE_LEGACY_KERAS', '1')
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
import tf_keras

ROOT = Path(__file__).resolve().parents[1]

def load_e1_model(e1_dir: Path):
    src = e1_dir / 'tfjs'
    config = json.loads((src / 'model.json').read_text(encoding='utf-8'))
    metadata = json.loads((src / 'metadata.json').read_text(encoding='utf-8'))
    model = tf_keras.models.model_from_json(json.dumps(config['modelTopology']))
    
    # Load weights from binary
    decoded = {}
    for group in config['weightsManifest']:
        raw = b''.join((src / name).read_bytes() for name in group['paths'])
        offset = 0
        for weight in group['weights']:
            count = int(np.prod(weight['shape']))
            decoded[weight['name']] = np.frombuffer(raw, dtype='<f4', count=count, offset=offset).reshape(weight['shape']).copy()
            offset += count * 4
            
    names = [w.name.split(':')[0] for w in model.weights]
    model.set_weights([decoded[name] for name in names])
    return model, config, metadata

def load_dataset(dataset_dir: Path, labels: list[str]):
    images = []
    targets = []
    for idx, label in enumerate(labels):
        label_dir = dataset_dir / label
        for img_path in sorted(label_dir.glob('*.jpg')):
            with Image.open(img_path) as img:
                img = ImageOps.exif_transpose(img).convert('RGB')
                img = ImageOps.fit(img, (224, 224), method=Image.Resampling.LANCZOS)
                arr = np.asarray(img, dtype=np.float32) / 127.5 - 1.0
                images.append(arr)
                targets.append(idx)
    X = np.stack(images, axis=0)
    y = tf_keras.utils.to_categorical(targets, num_classes=len(labels))
    return X, y

def save_tfjs_export(model, config, metadata, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    weights_dict = {w.name.split(':')[0]: w.numpy() for w in model.weights}
    
    manifest_weights = config['weightsManifest'][0]['weights']
    raw_bytes = bytearray()
    for item in manifest_weights:
        w_name = item['name']
        w_arr = weights_dict[w_name].astype('<f4')
        raw_bytes.extend(w_arr.tobytes())
        
    (out_dir / 'model.weights.bin').write_bytes(raw_bytes)
    
    # Update metadata
    meta = dict(metadata)
    meta['timeStamp'] = datetime.now(timezone.utc).isoformat()
    (out_dir / 'metadata.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    
    # Save model.json
    (out_dir / 'model.json').write_text(json.dumps(config, indent=2), encoding='utf-8')
    print(f"TFJS model saved to {out_dir}")

def main():
    e1_dir = ROOT / 'models' / 'experiments' / 'E1'
    e2_dir = ROOT / 'models' / 'experiments' / 'E2'
    data_dir = ROOT / 'dataset_public' / 'train_e2'
    
    print("Loading E1 model topology and base weights...")
    model, config, metadata = load_e1_model(e1_dir)
    labels = metadata['labels']
    print(f"Labels: {labels}")
    
    # Freeze the base feature extractor (layer 0: sequential_1)
    base_extractor = model.layers[0]
    base_extractor.trainable = False
    print("Base feature extractor frozen.")
    
    # Re-initialize the Dense head for independent training of E2
    head = model.layers[1]
    head.trainable = True
    
    # Load dataset
    print(f"Loading training data from {data_dir}...")
    X_train, y_train = load_dataset(data_dir, labels)
    print(f"Loaded {len(X_train)} images with shape {X_train.shape}.")
    
    # Compile
    optimizer = tf_keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Train for 100 epochs, batch size 16
    print("Training E2 for 100 epochs, batch size 16...")
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=16,
        shuffle=True,
        verbose=1
    )
    final_acc = float(history.history['accuracy'][-1])
    final_loss = float(history.history['loss'][-1])
    print(f"E2 Training Complete. Final Accuracy: {final_acc:.4f}, Final Loss: {final_loss:.4f}")
    
    # Save TFJS export
    e2_tfjs_dir = e2_dir / 'tfjs'
    save_tfjs_export(model, config, metadata, e2_tfjs_dir)
    
    # Convert to TFLite unquantized
    print("Converting E2 TFJS export to TFLite...")
    import subprocess
    import sys
    res = subprocess.run([sys.executable, str(ROOT / 'tools' / 'convert_tm_export.py'), str(e2_dir)],
                         capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("Conversion error:", res.stderr)
        sys.exit(1)
        
    print(f"E2 successfully created at {e2_dir}")

if __name__ == '__main__':
    main()
