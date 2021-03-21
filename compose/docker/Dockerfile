FROM python:3.8.5
LABEL description="Compose Editor - gethue.com"

ADD . /build

RUN mkdir /app
WORKDIR /app

# Should update OS packages

RUN python -m pip install --upgrade pip
# Should use a virtual env
#&& pip install virtualenv && python -m venv python_env

# SHELL ["/bin/bash", "-c"]
# RUN source python_env/bin/activate

RUN python -m pip install /build && rm -rf /build

# Should have a more elegant conf dir
COPY compose/docker/local_settings.py /usr/local/lib/python3.8/site-packages/compose/conf/local_settings.py
# COPY compose/docker/local_settings.py compose/conf/local_settings.py

COPY compose-ui/index.html compose-ui/build/index.html

COPY compose/docker/startup.sh .

# Should chown and use a compose user

# Should copy virtual env into new lean image and same with UI

EXPOSE 8005
ENTRYPOINT ["./startup.sh"]
