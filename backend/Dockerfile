FROM python:3.8

ENV APP_ROOT=/app/

RUN apt-get update \
    && apt-get install -y libsasl2-dev \
    python-dev \
    libldap2-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    mariadb-client \
    openssh-server \
    xmlsec1 \
    vim \
    sudo \
    logrotate \ 
    swig \
    less \
    supervisor 

WORKDIR ${APP_ROOT}

ADD ./src ${APP_ROOT}
COPY Pipfile Pipfile.lock ${APP_ROOT}

RUN pip install pipenv && pipenv install --dev

EXPOSE 8000
CMD pipenv run gunicorn --bind :8000 --workers 3 --reload gmop.wsgi
