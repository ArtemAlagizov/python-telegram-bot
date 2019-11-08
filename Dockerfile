FROM python:3.7
COPY . /app
WORKDIR /app
RUN python setup.py install
EXPOSE 5000
WORKDIR /app/itmo-bot
