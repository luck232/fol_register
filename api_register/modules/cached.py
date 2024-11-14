import redis

# Crear una conexión a Redis
class userIncriptionCache:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.cache_code = redis.Redis(host = self.host, port = self.port, db = 0) #para almacenar los  codigos enviados
        self.cache_name = redis.Redis(host = self.host, port = self.port, db = 1) #usuarios en registro pendiente
        self.cache_lock = redis.Redis(host = self.host, port = self.port, db = 2) #delay entre correos

    def locked_resend(self, username:str)-> bool:
        return self.cache_lock.exists(username)


    def submit_verification(self, username:str, public_code:str, private_code:str) :
        self.cache_code.hset(public_code, mapping = {'prcd': private_code, 'usr': username}) #subimos el codigo aleatorio para el usuario
        self.cache_code.expire(public_code, 30 * 60) #se puede registrar mientras la clave dura 30 minutos
        self.cache_name.hset(username, "cod", public_code) 
        self.cache_name.expire(username, 30 * 60) #vinculamos a el usuario con su codigo a enviar durrara 30 minutos
        self.cache_lock.hset(username, "0", "0")
        self.cache_lock.expire(username, 5 * 60) #queda 5 minutos para reenviar el correo


    def get_by_public(self, public_code:str):
        raw_data = self.cache_code.hgetall(public_code) #recibira el codigo enviado por el cliente
        data = {k.decode('utf-8'): v.decode('utf-8') for k, v in raw_data.items()}
        if data != {}:
            return data['prcd'], data['usr'] #retornamnos el codigo privado que se entrega en el registro
        return None, None


    def del_all(self, username:str):
        raw_data = self.cache_name.hgetall(username) #obtenemos el codigo de el usuario para eliminar las llaves relacionados a el
        data = {k.decode('utf-8'): v.decode('utf-8') for k, v in raw_data.items()}
        if data != {}:
            self.cache_code.delete(data["cod"])
            self.cache_name.delete(username)
            self.cache_lock.delete(username)
