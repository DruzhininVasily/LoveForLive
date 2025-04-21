FROM ubuntu:latest
MAINTAINER Druzhinin Vasily 'web_dev_drizhinin@mail.com'
RUN apt-get update -y --fix-missing
RUN apt-get install -y python3 python3-pip python-dev-is-python3 build-essential default-libmysqlclient-dev mysql-client pkg-config python3-venv
RUN adduser --disabled-password admin
RUN mkdir /home/loveforlive/ && chown -R admin:admin /home/loveforlive
RUN mkdir -p /var/log/loveforlive && touch /var/log/loveforlive/loveforlive.err.log && touch /var/log/loveforlive/loveforlive.out.log
RUN chown -R admin:admin /var/log/loveforlive

WORKDIR /home/loveforlive
USER admin
# copy all the files to the container
COPY --chown=admin:admin . .

# venv
ENV VIRTUAL_ENV=/home/loveforlive/venv

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# upgrade pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN python3 /home/loveforlive/manage.py migrate
RUN python3 /home/loveforlive/manage.py collectstatic --noinput

# define the port number the container should expose
EXPOSE 8000


#CMD ["gunicorn", "--workers", "4", "--timeout", "6000",  "--bind", ":8000", "LoveForLive.wsgi:application"]