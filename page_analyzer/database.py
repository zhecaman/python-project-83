import psycopg2
from datetime import date


class DataBase:

    """
    A class for working with database
    :params:
    A params to connect to database.
    """

    def __init__(self, db_url=None, **kwargs):
        if db_url is not None:
            self.connection = psycopg2.connect(db_url)
        else:
            self.connection = psycopg2.connect(**kwargs)
        self.__create_table()

    def get_url_id_if_exist(self, url):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM urls WHERE name = %s;", (url,))
            res = cursor.fetchone()
        if res:
            return res[0]
        return

    def add_to_urls(self, url):
        created_at = date.today()
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING (id);",
                (url, created_at),
            )
            id = cursor.fetchone()[0]
            self.connection.commit()
        return id

    def get_all_urls(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT urls.id, urls.name, url_checks.created_at, url_checks.status_code FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.url_id ORDER BY urls.id DESC;"""
            )
            res = cursor.fetchall()
        urls = []
        for row in res:
            url = {
                "id": row[0],
                "name": row[1],
                "created_at": row[2],
                "status_code": row[3],
            }
            urls.append(url)
        return urls

    def get_url(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM urls WHERE id = %s;", (id,))
            res = cursor.fetchone()
        id, name, created_at = res
        url = {"id": id, "name": name, "created_at": created_at}
        return url

    def add_to_checks(self, id, code):
        created_at = date.today()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO url_checks (url_id, created_at, status_code) VALUES (%s,%s, %s);
                """,
                (id, created_at, code),
            )
            self.connection.commit()

    def update_check(self, id, query):
        updated_at = date.today()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE url_checks SET (status_code, h1, title, description, created_at) = (%s,%s, %s, %s, %s) WHERE url_id = %s;
        """,
                (*query, updated_at, id),
            )

    def get_all_checks_by_id(self, id):
        checks = []
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM url_checks WHERE (url_id) = %s ORDER BY id DESC;""",
                (id,),
            )

            for row in cursor.fetchall():
                check = {
                    "id": row[0],
                    "url_id": row[1],
                    "status_code": row[2],
                    "h1": row[3],
                    "title": row[4],
                    "description": row[5],
                    "created_at": row[6],
                }
                checks.append(check)
        return checks

    def __create_table(self, sql_file="database.sql"):
        with open(sql_file, "r") as file:
            self.connection.cursor().execute(file.read())

    def close(self):
        self.connection.close()
