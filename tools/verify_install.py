"""Smoke test the installed, real model without starting an HTTP server."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from PIL import Image
from app.inference import TFLiteClassifier


def main():
    model = TFLiteClassifier(ROOT / 'models/tflite')
    expected = json.loads((ROOT / 'evidence/testing/FINAL_E2.json').read_text())['model_id']
    if model.model_id != expected:
        raise RuntimeError('Model aktif tidak sepadan dengan model E2 yang dinilai.')
    sample = ROOT / 'dataset_public/test/BOTOL/049d99faa622b032.jpg'
    with Image.open(sample) as image:
        result = model.predict(image, .7)
    if result['prediction'] != 'BOTOL':
        raise RuntimeError(f'Ramalan smoke test tidak dijangka: {result}')
    print(json.dumps({'status': 'PASS', 'runtime': 'Google LiteRT',
                     'model_id': model.model_id, 'sample': str(sample.relative_to(ROOT)),
                     'result': result}, indent=2))


if __name__ == '__main__':
    main()
