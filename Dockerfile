FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt requirements-model.txt ./
RUN pip install --no-cache-dir -r requirements-model.txt
COPY app ./app
COPY static ./static
COPY models ./models
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
