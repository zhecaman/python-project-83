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
    
    
    def get_id_if_exist(self, url):
        """
        Args:
            url (str): _description_

        Returns:
            bool: _description_
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM urls WHERE name = %s;", (url,)
            )
            return cursor.fetchone()
        
        
    def add_url(self, url):
        
        created_at = str(date.today())
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING (id);", (url, created_at) 
            )
            id = cursor.fetchone()[0]
            self.connection.commit()
            return id
    
    
    def get_all_urls(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM urls")
        res = cursor.fetchall()
        urls = []
        for row in res:
            url = {
                'id' : row[0],
                'name' : row[1],
                'created_at' : row[2]
            }
            urls.append(url)
        return urls
    
    
    def get_url(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM urls WHERE id = %s;", (id,)
            )
            _id, name, created_at = cursor.fetchone()
            url = {
                'id': _id,
                'name': name, 
                'created_at': created_at
            }
            return url

    def __create_table(self, sql_file='database.sql'):
        with open(sql_file, 'r') as file:
            self.connection.cursor().execute(file.read())
        
        
    def close(self):
        self.connection.close()