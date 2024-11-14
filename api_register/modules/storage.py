import mariadb 

class usersdb:
    def __init__(self, config:dict):
        self.config = config
        self.connect_database()

    def connect_database(self):
        connection = mariadb.connect(
            **self.config
        )
        return connection

    def exist_user(self, username:str)-> bool:
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.callproc("sp_exist_user", (username,))
        
        for result in cursor.fetchall():
            return bool(result[0]) #retorna 1 existe
        conn.close()

    def create_user(self, username:str, shapass:str)-> bool:
        conn = self.connect_database()
        cursor = conn.cursor()
        cursor.callproc("sp_create_user", (username, shapass))
        
        for result in cursor.fetchall():
            conn.close()
            return bool(result[0]) #operacion exitosa si retorna 1
        return False
    
