FROM python:3.8

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

WORKDIR /app

ADD ./src /app/
COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --dev

CMD pipenv run python manage.py migrate --noinput && \ 
    pipenv run gunicorn --bind :80 --workers 3 --reload gmop.wsgi
