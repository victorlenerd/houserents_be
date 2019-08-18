FROM python:3

WORKDIR /home/houserents

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY controllers controllers
COPY db db
COPY main.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

EXPOSE 5000

CMD ["./boot.sh"]