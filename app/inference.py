"""Inference for the FLOAT (unquantized) Teachable Machine TFLite export."""
from pathlib import Path
import re
import threading
import hashlib
import numpy as np
from PIL import Image, ImageOps


def read_labels(path: Path) -> list[str]:
    labels = [re.sub(r'^\d+\s+', '', line.strip()) for line in
              path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    if len(labels) < 3 or len(set(labels)) != len(labels):
        raise ValueError('labels.txt mesti mempunyai sekurang-kurangnya 3 label unik.')
    return labels


def preprocess(image: Image.Image, size: tuple[int, int]) -> np.ndarray:
    image = ImageOps.exif_transpose(image).convert('RGB')
    image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
    return np.expand_dims(np.asarray(image, dtype=np.float32) / 127.5 - 1.0, 0)


def format_prediction(labels, values, threshold):
    scores = np.asarray(values, dtype=float).reshape(-1)
    if len(scores) != len(labels) or not np.all(np.isfinite(scores)):
        raise ValueError('Output model tidak sepadan dengan label atau tidak sah.')
    if np.any(scores < 0) or np.any(scores > 1) or not np.isclose(scores.sum(), 1, atol=.03):
        raise ValueError('Model mesti mengeluarkan kebarangkalian softmax.')
    best = int(np.argmax(scores))
    confidence = float(scores[best])
    accepted = confidence >= threshold
    return dict(prediction=labels[best] if accepted else 'UNKNOWN',
                top_class=labels[best], confidence=confidence,
                status='recognized' if accepted else 'low_confidence',
                threshold=threshold,
                scores=[dict(label=label, confidence=float(score))
                        for label, score in zip(labels, scores)])


class TFLiteClassifier:
    def __init__(self, model_dir: Path):
        model_path = model_dir / 'model_unquant.tflite'
        labels_path = model_dir / 'labels.txt'
        if not model_path.exists() or not labels_path.exists():
            raise FileNotFoundError('Letak model_unquant.tflite dan labels.txt di models/tflite, kemudian mula semula server.')
        from ai_edge_litert.interpreter import Interpreter
        self.labels = read_labels(labels_path)
        self.model_id = hashlib.sha256(model_path.read_bytes() + b'\0' + labels_path.read_bytes()).hexdigest()
        self.interpreter = Interpreter(model_path=str(model_path), num_threads=2)
        self.interpreter.allocate_tensors()
        inputs = self.interpreter.get_input_details()
        outputs = self.interpreter.get_output_details()
        if len(inputs) != 1 or len(outputs) != 1:
            raise ValueError('Model mesti mempunyai satu input dan satu output.')
        self.input, self.output = inputs[0], outputs[0]
        shape = self.input['shape'].tolist()
        if len(shape) != 4 or shape[0] != 1 or shape[3] != 3:
            raise ValueError('Input model mesti berbentuk [1, tinggi, lebar, 3].')
        if self.input['dtype'] != np.float32 or self.output['dtype'] != np.float32:
            raise ValueError('Pilih eksport TensorFlow Lite FLOAT / unquantized.')
        if int(np.prod(self.output['shape'])) != len(self.labels):
            raise ValueError('Bilangan label berbeza daripada output model.')
        self.size = (shape[2], shape[1])
        self.lock = threading.Lock()

    def predict(self, image, threshold):
        batch = preprocess(image, self.size)
        with self.lock:
            self.interpreter.set_tensor(self.input['index'], batch)
            self.interpreter.invoke()
            scores = self.interpreter.get_tensor(self.output['index']).copy()
        return format_prediction(self.labels, scores, threshold)
