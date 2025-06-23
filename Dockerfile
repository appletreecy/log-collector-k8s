FROM python:3.11-slim
WORKDIR /app
COPY ./app/collector.py .
RUN pip install fastapi uvicorn elasticsearch
CMD ["uvicorn", "collector:app", "--host", "0.0.0.0", "--port", "8080"]
