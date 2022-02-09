FROM python:3.6-alpine

RUN apk update && apk upgrade && python -m pip install --upgrade pip

RUN adduser \
    --disabled-password \
    --gecos "app user" \
    --home "/app" \
    --no-create-home \
    "app"

WORKDIR /app/

RUN chown -R app:app .

USER app

COPY . .

RUN pip3.6 install -r requirements.txt

EXPOSE 9119
ENTRYPOINT [ "/bin/sh",  "entrypoint.sh" ]
