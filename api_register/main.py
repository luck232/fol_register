from flask import Flask, request, jsonify
from modules import cached, storage, send_code, utils
from dotenv import load_dotenv
import os

###cargar variables de entrono

load_dotenv()
credetial_database = {
"host": os.getenv("MYSQL_HOST"),
"user": os.getenv("MYSQL_USER"),
"password": os.getenv("MYSQL_PASSWORD"),
"database": os.getenv("MYSQL_DB")
}
smtp_mail = {
"server":os.getenv("SMTP_SERVER"),
"username":os.getenv("SMTP_USERNAME"),
"password":os.getenv("SMTP_PASSWORD"),
"port":int(os.getenv("SMTP_PORT"))
}
redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT'))


viapass = cached.userIncriptionCache(redis_host, redis_port)
database = storage.usersdb(credetial_database)
app = Flask(__name__)


@app.route('/getviapass', methods=['GET'])
def get_intern_indentity():
    try:
        public_code = request.args.get('pu_code') #obtener codigo
    except:
        return({"error": "broken format"}, 400)
    if not utils.is_code(public_code): 
        return jsonify({"error": "broken format"} ,400) #no cumple condiciones de codigo
    private_code, username = viapass.get_by_public( utils.to_sha(public_code)) #obtener codigo interno y su usuario
    if username == None:
        return jsonify({"status": "missed"}, 200)
    return jsonify({"pr_code": private_code, "username" : username}, 200) #entregar codigo interno y usuario


@app.route('/send_verify', methods=['POST'])
def send_verify():
    data = request.get_json()
    try:
        username = data.get('username')  #obtener el correo de usuario
    except:
        return jsonify({"error": "broken format"}, 400) 
    if not utils.is_email(username):# cumple codiciones de email
        return({"error": "broken format"}, 400) 
    elif database.exist_user(username): #el usuario existe?
        return jsonify({"error": "duplied"}, 400)
    
    if viapass.locked_resend(username): 
        return jsonify({"status": "wait"}, 200) #debe esperar para reenviar
    else:  #aqui no importa si el usuario ya esta en espera se elimina cualquier dato relacionado con el usaurio para reenviar el codigo
        viapass.del_all(username) 
        public_code = utils.unique_code()
        private_code = utils.unique_code()
        viapass.submit_verification(username, utils.to_sha(public_code), private_code)
        send_code.verify(username, public_code, smtp_mail["server"], smtp_mail["port"], smtp_mail["username"], smtp_mail["password"])
    
    return jsonify({"status": "sended"}, 200) #enviado


@app.route('/registration', methods=['POST'])
def registration():
    data = request.get_json()
    try:  #obtenemos el codigo privado, publico, username, password y repassword
        private_code_inp = data.get('pr_code')
        public_code = data.get('pu_code')
        username_inp = data.get('username')
        password = data.get('password')
        repassword = data.get('repassword')
    except:
        return({"error": "broken format"}, 400) #faltan datos 
    if not utils.is_code(public_code) or not utils.is_code(private_code_inp) or not utils.is_password(password):#los codigos o contraseñas no cumplen
        return({"error": "broken format"}, 400)
    if password != repassword: #las contraseñas coinciden?
        return jsonify({"error": "broken match"})
    private_code, username = viapass.get_by_public( utils.to_sha(public_code)) #busco retorna el codigo privado y usarname
    if username == None: 
        return jsonify({"status": "missed"}, 200) #el codigo no fue encontrado
    if private_code != private_code_inp or username_inp != username: #coincide el servidor con el cliente
        return jsonify({"status": "broken info"}, 200)
    viapass.del_all(username) #limpio los datos de usaurio del cache
    if database.create_user(username, utils.hashpass(password)): #registro usuario con contraseña hasheada
        return jsonify({"status": "registed"}, 200)
    return jsonify({"error": "crashed"}, 500)#error misentras se registraba
    
if __name__ == '__main__':
    app.run(debug=True)
