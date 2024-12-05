
from DAO.Conexion import Conexion
import bcrypt


host='localhost'
user='userempresa'
passwordS='V3ntana.13'
db='empresa'

class Usuario:
    def __init__(self, username, password_hash, nombre, apellidos, email, tipo_usuario):
        self.username = username
        self.password_hash = password_hash
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.tipo_usuario = tipo_usuario
    
    @staticmethod
    def login(username, password):
        con = Conexion(host, user, passwordS, db)
        usuario_data = con.obtenerUsuario(username)

        if usuario_data and len(usuario_data) > 0:
            usuario_data = usuario_data[0]
            hashed_password = usuario_data[2].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return Usuario(
                    username=usuario_data[1],
                    password_hash=usuario_data[2],
                    nombre=usuario_data[3],
                    apellidos=usuario_data[4],
                    email=usuario_data[5],
                    tipo_usuario=usuario_data[6]
                )
        return None
    
    @staticmethod
    def registrar_usuario(username, password, nombre, apellidos, email, tipo_usuario):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        nuevo_usuario = Usuario(
            username=username,
            password_hash=hashed_password,
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            tipo_usuario=tipo_usuario
        )

        con = Conexion(host, user, passwordS, db)
        exito = con.agregarUsuario(
            username=nuevo_usuario.username,
            password_hash=nuevo_usuario.password_hash.decode('utf-8'),
            nombre=nuevo_usuario.nombre,
            apellidos=nuevo_usuario.apellidos,
            email=nuevo_usuario.email,
            tipo_usuario=nuevo_usuario.tipo_usuario
        )

        if exito:
            print("¡Usuario registrado exitosamente!")
            return nuevo_usuario
        else:
            print("Error al registrar el usuario")
            return None