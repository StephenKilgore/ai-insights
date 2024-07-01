FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python scripts/wait_for_services.py && gunicorn -b 0.0.0.0:8080 app:app"]
