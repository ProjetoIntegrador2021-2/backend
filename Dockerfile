FROM python:3.10-alpine
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev \
    && apk add --no-cache mariadb-dev
RUN pip install -U pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN apk del build-deps
WORKDIR /usr/share/app
COPY . .
EXPOSE 5000
ENTRYPOINT [ "sh", "entrypoint.sh" ]