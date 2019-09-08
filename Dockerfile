FROM python:3

RUN mkdir -p /usr/src/hourserents
WORKDIR /usr/src/hourserents

COPY requirements-prod.txt /usr/src/hourserents/
COPY numpy-1.16.1-cp37-cp37m-manylinux1_x86_64.whl /usr/src/hourserents/
COPY pandas-0.23.0.tar.gz /usr/src/hourserents/

RUN pip install --upgrade pip
RUN pip install -r requirements-prod.txt

RUN pip install numpy-1.16.1-cp37-cp37m-manylinux1_x86_64.whl
RUN pip install pandas-0.23.0.tar.gz

COPY controllers /usr/src/hourserents/controllers
COPY db /usr/src/hourserents/db
COPY misc /usr/src/hourserents/misc
COPY main.py boot.sh test_main.py __init__.py /usr/src/hourserents/

RUN chmod +x boot.sh

ARG ENV
ARG DB_HOST
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_PORT
ARG DATA_SERVER
ARG REDIS_HOST
ARG REDIS_PORT
ARG REDIS_PASSWORD

RUN echo $DB_HOST

RUN echo $DB_USER

ENV FLASK_APP main.py
RUN python -m unittest test_main.py

EXPOSE 5000

CMD ["./boot.sh"]
