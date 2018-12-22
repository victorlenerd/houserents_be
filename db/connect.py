import psycopg2
import os

def connect(host, db_name, db_user, db_password):
    conn = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password)        

def populateTable():
    