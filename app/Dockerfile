FROM python:3.13-alpine

WORKDIR /app

RUN pip install --no-cache-dir Flask==3.1.1

COPY app.py .

CMD ["python", "app.py"]
