FROM python:3.6-alpine

RUN adduser -D houserents

WORKDIR /home/houserents

COPY requirements.txt requirements.txt
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN python -m venv venv
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY controllers controllers
COPY model model
COPY db db
COPY view view
COPY main.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R houserents:houserents ./
USER houserents

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]