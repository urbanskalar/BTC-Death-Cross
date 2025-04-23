FROM ubuntu:latest

WORKDIR /app

RUN apt-get update
RUN apt-get -y install cron python3 python3-pip

ENV PIP_BREAK_SYSTEM_PACKAGES=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY deathCross.py .

COPY crontab /etc/cron.d/death-cross-cron
RUN chmod 0644 /etc/cron.d/death-cross-cron
RUN crontab /etc/cron.d/death-cross-cron
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log

CMD ["python", "deathCross.py"]
