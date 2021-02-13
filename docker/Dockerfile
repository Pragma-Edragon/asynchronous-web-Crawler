FROM python:3.8.7-alpine3.12

COPY . /app
WORKDIR /app

RUN apk add libxml2-dev libxslt-dev build-base
RUN pip --disable-pip-version-check --no-cache-dir \
    install -r ./docker/requirements.txt


RUN addgroup -S crawlergroup && adduser -S crawleruser -G crawlergroup
USER crawleruser

CMD ["python", "/app/app.py"]
