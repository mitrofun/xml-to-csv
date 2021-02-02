FROM python:3.9.1-alpine3.12

COPY requirements.txt /opt/app/

RUN pip3 install --upgrade pip setuptools \
	&& pip3 install --no-cache-dir -r /opt/app/requirements.txt

COPY . /opt/app

WORKDIR /opt/app/