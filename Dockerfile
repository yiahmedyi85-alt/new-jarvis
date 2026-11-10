FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY cloud_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY cloud_service /app/cloud_service
WORKDIR /app
EXPOSE 8000

CMD ["uvicorn", "cloud_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
