FROM python:3

WORKDIR /home/houserents

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY controllers controllers
COPY db db
COPY main.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

ENV ENV production
ENV DB_HOST ${DB_HOST}
ENV DB_NAME ${DB_NAME}
ENV DB_USER ${DB_USER}
ENV DB_PASSWORD ${DB_PASSWORD}
ENV DB_PORT ${DB_PORT}
ENV DATA_SERVER ${DATA_SERVER}

EXPOSE 5000

CMD ["gunicorn -b :5000 --access-logfile - --error-logfile - main:app"]