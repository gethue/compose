FROM ubuntu:20.04
LABEL description="Compose API - gethue.com"

RUN apt-get update -y && apt-get install -y \
  python3-pip \
  #libmariadb-dev-compat \
  libssl-dev \
  libmysqlclient-dev \
  python3-venv

ADD . /hue
WORKDIR /hue

RUN pip3 install virtualenv && python3 -m venv python_env

SHELL ["/bin/bash", "-c"]
RUN source python_env/bin/activate

RUN pip3 install -r requirements.txt

# COPY core/local_settings.py.tmpl core/local_settings.py
COPY docker/startup.sh .

EXPOSE 8000
CMD ["./startup.sh"]
