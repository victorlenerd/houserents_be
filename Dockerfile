FROM python:3

WORKDIR /home/houserents

COPY requirements.txt requirements.txt
# RUN apk update
# RUN apk upgrade
# RUN apk add
# RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
# RUN python -m venv venv
RUN pip install -r requirements.txt

COPY controllers controllers
COPY db db
COPY main.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

# RUN chown -R houserents:houserents ./
# USER houserents

EXPOSE 5000

# ENTRYPOINT ["./boot.sh"]