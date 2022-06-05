# Stage 1 - Install build dependencies
FROM python:3.9-slim AS builder

ADD ./requirements.txt /

RUN pip install --prefix=/install --ignore-installed -r requirements.txt

# Stage 2 - Copy only necessary files to the runner stage
FROM python:3.9-slim

#RUN apt-get update && apt-get install -y cron

COPY --from=builder /install /usr/local

WORKDIR /home/tuandc/code

COPY . .
COPY entry-point.sh .
#COPY supervisord.conf /etc/supervisor/supervisord.conf

#RUN echo "*/15 * * * * root cd /home/tuandc/code && ./cron.sh > /proc/1/fd/1 2>&1" >> /etc/crontab && sed -i -e 's/\r$//' entry-point.sh && chmod +x entry-point.sh && ls -la && sed -i -e 's/\r$//' cron.sh && chmod +x cron.sh

RUN sed -i -e 's/\r$//' entry-point.sh
RUN chmod +x entry-point.sh

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["./entry-point.sh"]
