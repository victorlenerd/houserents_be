FROM python:3

RUN mkdir -p /usr/src/hourserents
WORKDIR /usr/src/hourserents

COPY requirements.txt /usr/src/hourserents/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY controllers /usr/src/hourserents/
COPY db /usr/src/hourserents/
COPY main.py boot.sh /usr/src/hourserents/
RUN chmod +x boot.sh

ENV FLASK_APP main.py
ENV PORT ${PORT}

EXPOSE ${PORT}

CMD python main.py