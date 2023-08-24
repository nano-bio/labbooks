FROM node:18-alpine AS django-npm-builder

WORKDIR /builds
COPY package.json gulpfile.js ./
RUN npm install

FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install --no-install-recommends -y cron

WORKDIR /src

COPY --from=django-npm-builder /builds/src/_vendor ./_vendor/

COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/nano-bio/fitlib.git@package

COPY ./src .

ADD /entrypoint.sh /etc/entrypoint.sh
ENTRYPOINT ["/bin/sh", "/etc/entrypoint.sh"]
