import psycopg2
import os

root_dir = os.path.dirname(__file__)

def connectDB(host, db_name, db_user, db_password, db_port):
    conn = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password, port=db_port)
    curr = conn.cursor()
    sql_file_path = os.path.join(root_dir, 'db.pgsql');
    print(sql_file_path)
    with open(sql_file_path, 'r') as pssql:
        query = pssql.read().encode("utf8")
        curr.execute(query)

    return conn