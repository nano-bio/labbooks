FROM python:3.9
ENV PYTHONUNBUFFERED 1

#RUN apt-get update
#RUN apt-get install --no-install-recommends -y cron
#RUN cron

WORKDIR /src

COPY ./config/pip/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/nano-bio/fitlib.git@package

COPY . .

ADD /entrypoint.sh /etc/entrypoint.sh
ENTRYPOINT ["/bin/sh", "/etc/entrypoint.sh"]
