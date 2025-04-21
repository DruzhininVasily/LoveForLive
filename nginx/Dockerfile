FROM nginx:latest
MAINTAINER Druzhinin Vasily 'web_dev_drizhinin@mail.com'

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python-dev-is-python3 build-essential python3-venv python3-setuptools net-tools htop python3-certbot-nginx -y
RUN adduser --disabled-password admin
RUN mkdir /home/loveforlive_nginx/ && chown -R admin:admin /home/loveforlive_nginx

ENV VIRTUAL_ENV=/home/loveforlive_nginx/venv

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/

#RUN certbot --nginx -d love-for-live.ru -d www.love-for-live.ru


