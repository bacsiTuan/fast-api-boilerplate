FROM python:3.9-slim as builder

RUN mkdir /install
WORKDIR /install

RUN apt-get update \
    && apt-get install git -y \
    && apt-get install -y --reinstall ca-certificates \
    && pip install pipenv
#    && pip install toml


COPY requirements.txt .
RUN pip install --prefix=/install --ignore-installed -r requirements.txt


FROM python:3.9-slim
#RUN apt-get update && apt-get install -y cron

ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /home/tuandc

WORKDIR /home/tuandc

COPY --from=builder /install /usr/local
#COPY app/ app/
#COPY fast_api_app/ fast_api_app/
#COPY grpc_app/ grpc_app/
#COPY schemas/ schemas/

#COPY entry-point.sh .
#COPY manage.py manage.py
#COPY fast_api_manage.py fast_api_manage.py
#COPY grpc_manage.py grpc_manage.py
COPY . .

#COPY Makefile Makefile
COPY supervisord.conf /etc/supervisor/supervisord.conf

#RUN echo "*/15 * * * * root cd /home/tuandc/code && ./cron.sh > /proc/1/fd/1 2>&1" >> /etc/crontab && sed -i -e 's/\r$//' entry-point.sh && chmod +x entry-point.sh && ls -la && sed -i -e 's/\r$//' cron.sh && chmod +x cron.sh

RUN sed -i -e 's/\r$//' entry-point.sh
RUN chmod +x entry-point.sh


EXPOSE 8000

ENTRYPOINT ["./entry-point.sh"]
