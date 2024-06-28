FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y cron
COPY collector-cron /etc/cron.d/collector-cron
RUN chmod 0644 /etc/cron.d/collector-cron
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/collector-cron
CMD ["cron", "-f"]
