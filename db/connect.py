import psycopg2
import os

root_dir = os.path.dirname(__file__)

class DBConnector:

    class __DBConnector:

        def __init__(self, host, db_name, db_user, db_password, db_port):
            conn = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password, port=db_port)

            sql_file_path = os.path.join(root_dir, 'db.pgsql')

            with conn.cursor() as curr:
                with open(sql_file_path, 'r') as pg_sql:
                    query = pg_sql.read().encode("utf8")
                    curr.execute(query)
                conn.commit()

            self.db_context = conn

    instance = None

    def __init__(self, host, db_name, db_user, db_password, db_port):
        if not DBConnector.instance:
            DBConnector.instance = DBConnector.__DBConnector(host, db_name, db_user, db_password, db_port)
