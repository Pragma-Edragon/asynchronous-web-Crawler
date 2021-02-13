FROM 3.8.7-alpine3.13

COPY /crawler/. /app
WORKDIR /app

RUN pip --disable-pip-version-check --no-cache-dir \
    install -r ./requirements.txt

RUN addgroup -S crawlergroup && adduser -S crawleruser -G crawlergroup
USER crawleruser

CMD ["python /app/app.py"]