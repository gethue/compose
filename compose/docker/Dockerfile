FROM python:3.8.5
LABEL description="Compose API - gethue.com"

ADD . /app
WORKDIR /app

RUN python -m pip install --upgrade pip && pip install virtualenv && python -m venv python_env

SHELL ["/bin/bash", "-c"]
RUN source python_env/bin/activate

RUN python -m pip install /app

# COPY core/local_settings.py.tmpl core/local_settings.py
COPY compose/docker/startup.sh .

# Should copy virtual env into new lean image and same with UI

EXPOSE 8005
ENTRYPOINT ["./startup.sh"]
