from io import BytesIO
import numpy as np
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.inference import format_prediction, preprocess, read_labels


@pytest.fixture
def client():
    with TestClient(app) as c:
        # Contract tests deliberately use no trained model.
        app.state.classifier = None
        yield c


def image_bytes():
    out = BytesIO()
    Image.new('RGB', (50, 40), (255, 0, 0)).save(out, 'PNG')
    return out.getvalue()


def test_home_and_health(client):
    assert client.get('/').status_code == 200
    assert client.get('/health').json()['model_ready'] is False


def test_no_model_is_explicit(client):
    assert client.post('/predict', files={'file': ('a.png', image_bytes())}).status_code == 503


@pytest.mark.parametrize('data,code', [(b'', 400), (b'not an image', 400), (b'x' * (8*1024*1024+1), 413)], ids=['empty','corrupt','oversize'])
def test_invalid_input(client, data, code):
    assert client.post('/predict', files={'file': ('a.png', data)}).status_code == code


def test_threshold_validation(client):
    assert client.post('/predict?threshold=1.1', files={'file': ('a.png', image_bytes())}).status_code == 422


def test_success_contract_with_test_double(client):
    class Stub:
        model_id = 'test-double-not-a-trained-model'
        labels = ['BOTOL', 'BUKU', 'TELEFON']
        def predict(self, image, threshold):
            return format_prediction(self.labels, [.8, .1, .1], threshold)
    app.state.classifier = Stub()
    response = client.post('/predict', files={'file': ('a.png', image_bytes())})
    assert response.status_code == 200
    assert response.json()['prediction'] == 'BOTOL'
    assert response.json()['model_id'] == 'test-double-not-a-trained-model'
    response = client.post('/predict?threshold=.9', files={'file': ('a.png', image_bytes())})
    assert response.json()['prediction'] == 'UNKNOWN'


def test_threshold_boundary():
    assert format_prediction(['A','B','C'], [.7,.2,.1], .7)['prediction'] == 'A'
    assert format_prediction(['A','B','C'], [.699,.201,.1], .7)['prediction'] == 'UNKNOWN'


def test_preprocessing():
    data=preprocess(Image.new('RGB',(400,100),(255,0,0)),(224,224))
    assert data.shape==(1,224,224,3)
    assert data.dtype==np.float32
    np.testing.assert_array_equal(data[0,0,0],[1,-1,-1])


def test_bad_scores():
    with pytest.raises(ValueError):
        format_prediction(['A','B','C'], [float('nan'),0,0], .7)
    with pytest.raises(ValueError):
        format_prediction(['A','B','C'], [.9,.9,.9], .7)


def test_labels(monkeypatch):
    from pathlib import Path
    path=Path('labels.txt')
    monkeypatch.setattr(Path, 'read_text', lambda *args, **kwargs: '0 BOTOL\n1 BUKU\n2 TELEFON\n')
    assert read_labels(path)==['BOTOL','BUKU','TELEFON']
