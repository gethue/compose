FROM python:3.8.5
LABEL description="Compose API - gethue.com"

ADD . /build

RUN mkdir /app
WORKDIR /app

# Should update OS packages

RUN python -m pip install --upgrade pip
#&& pip install virtualenv && python -m venv python_env

# SHELL ["/bin/bash", "-c"]
# RUN source python_env/bin/activate

RUN python -m pip install /build && rm -rf /build

# COPY compose/conf/local_settings.py.tmpl compose/conf/local_settings.py
COPY compose/docker/startup.sh .
RUN mkdir conf

# Should chown and use compose user

# Should copy virtual env into new lean image and same with UI

EXPOSE 8005
ENTRYPOINT ["./startup.sh"]
