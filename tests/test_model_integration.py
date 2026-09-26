"""Real exported models: verify the LiteRT migration against frozen evidence."""
import csv
import hashlib
import json
from pathlib import Path

from PIL import Image
import pytest
from app.inference import TFLiteClassifier

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('version,split,record', [
    ('E1', 'validation', 'validation/E1'),
    ('E2', 'validation', 'validation/E2'),
    ('E2', 'test', 'testing/FINAL_E2'),
])
def test_real_model_preserves_recorded_predictions(version, split, record):
    model = TFLiteClassifier(ROOT / 'models/experiments' / version / 'tflite')
    summary = json.loads((ROOT / 'evidence' / (record + '.json')).read_text())
    assert model.model_id == summary['model_id']
    with (ROOT / 'evidence' / (record + '.csv')).open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == summary['total'] == 30
    for row in rows:
        path = ROOT / row['file'].replace('\\', '/')
        assert path.parent.parent.name == split
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
        with Image.open(path) as image:
            result = model.predict(image, float(row['threshold']))
        assert result['top_class'] == row['top_class'], path.name
        assert result['prediction'] == row['prediction'], path.name
        assert result['confidence'] == pytest.approx(float(row['confidence']), abs=1e-4)
