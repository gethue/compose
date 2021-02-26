FROM python:3.8.5
LABEL description="Compose API - gethue.com"

RUN apt-get update -y && apt-get install -y \
  python3-pip \
  # libmariadb-dev-compat \
  # Needed below?
  # libssl-dev \
  # libmysqlclient-dev \
  python3-venv

ADD . /compose/compose
WORKDIR /compose

RUN pip3 install virtualenv && python3 -m venv python_env

SHELL ["/bin/bash", "-c"]
RUN source python_env/bin/activate

RUN pip3 install -r compose/requirements.txt

# Should copy virtual env into new lean image and same with UI

# COPY core/local_settings.py.tmpl core/local_settings.py
COPY docker/startup.sh .

EXPOSE 8005
CMD ["./startup.sh"]
