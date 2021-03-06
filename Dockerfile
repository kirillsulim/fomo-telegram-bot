FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY config.yaml .
COPY fomo_bot/ ./fomo_bot

CMD ["python3", "./main.py"]
