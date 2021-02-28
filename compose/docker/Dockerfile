FROM python:3.8.5
LABEL description="Compose API - gethue.com"

# Use virtual env again for lean image?
# Delete cache?
# RUN apt-get update -y && apt-get install -y \
#   python3-pip \
#   # libmariadb-dev-compat \
#   # Needed below?
#   # libssl-dev \
#   # libmysqlclient-dev \
#   python3-venv

ADD . /app
WORKDIR /app

# RUN python -m pip install --upgrade pip && pip install virtualenv && python -m venv python_env

# SHELL ["/bin/bash", "-c"]
# RUN source python_env/bin/activate

RUN pip install -r compose/requirements.txt

# Should copy virtual env into new lean image and same with UI

# COPY core/local_settings.py.tmpl core/local_settings.py
COPY compose/docker/startup.sh .

EXPOSE 8005
ENTRYPOINT ["./startup.sh"]
