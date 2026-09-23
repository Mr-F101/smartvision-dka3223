from contextlib import asynccontextmanager
from io import BytesIO
from pathlib import Path
from typing import Annotated, Literal
import logging
import os
import warnings
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from PIL import Image, UnidentifiedImageError
from starlette.concurrency import run_in_threadpool
from .inference import TFLiteClassifier

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 8 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 16_000_000
logger = logging.getLogger(__name__)


class Score(BaseModel):
    label: str
    confidence: float = Field(ge=0, le=1)


class Prediction(BaseModel):
    model_id: str
    prediction: str
    top_class: str
    confidence: float = Field(ge=0, le=1)
    status: Literal['recognized', 'low_confidence']
    threshold: float = Field(ge=0, le=1)
    scores: list[Score]


@asynccontextmanager
async def lifespan(app):
    app.state.classifier = None
    app.state.model_message = 'Model belum tersedia.'
    try:
        model_dir = Path(os.environ.get('MODEL_DIR', str(ROOT / 'models' / 'tflite')))
        app.state.classifier = await run_in_threadpool(TFLiteClassifier, model_dir)
        app.state.model_message = 'Model TensorFlow Lite tersedia.'
    except FileNotFoundError as exc:
        app.state.model_message = str(exc)
    except ImportError:
        app.state.model_message = 'Pasang requirements-model.txt untuk mengaktifkan inferens Python.'
    except Exception:
        logger.exception('Model failed to load')
        app.state.model_message = 'Model gagal dimuat. Semak eksport FLOAT, labels.txt dan log server.'
    yield


app = FastAPI(title='SmartVision Object Classifier', version='1.0.0', lifespan=lifespan)
app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')
app.mount('/models/tfjs', StaticFiles(directory=ROOT / 'models' / 'tfjs'), name='tfjs')


@app.get('/', include_in_schema=False)
def home():
    return FileResponse(ROOT / 'static' / 'index.html')


@app.get('/health')
def health():
    model = app.state.classifier
    return {'status': 'ok', 'model_ready': model is not None,
            'message': app.state.model_message, 'labels': model.labels if model else [],
            'model_id': model.model_id if model else None}


def decode_image(data):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            image = Image.open(BytesIO(data))
            if image.format not in {'JPEG', 'PNG', 'WEBP'}:
                raise HTTPException(415, 'Gunakan imej JPEG, PNG atau WebP.')
            image.load()
            return image
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(400, 'Fail bukan imej yang sah atau rosak.')
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(413, 'Resolusi imej terlalu besar. Had 16 megapiksel.')


@app.post('/predict', response_model=Prediction)
async def predict(file: Annotated[UploadFile, File()],
                  threshold: Annotated[float, Query(ge=0, le=1)] = .7):
    try:
        data = await file.read(MAX_BYTES + 1)
    finally:
        await file.close()
    if not data:
        raise HTTPException(400, 'Fail imej kosong.')
    if len(data) > MAX_BYTES:
        raise HTTPException(413, 'Had saiz fail ialah 8 MB.')
    image = await run_in_threadpool(decode_image, data)
    try:
        if app.state.classifier is None:
            raise HTTPException(503, app.state.model_message)
        model = app.state.classifier
        result = await run_in_threadpool(model.predict, image, threshold)
        return {**result, 'model_id': model.model_id}
    finally:
        image.close()
