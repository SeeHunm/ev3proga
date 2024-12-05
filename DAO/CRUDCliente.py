from DAO.Conexion import Conexion
from os import system

host = 'localhost'
user = 'userempresa'
password = 'V3ntana.13'
db = 'empresa'

def agregar(c):
    try:
        con = Conexion(host, user, password, db)
        sql = "INSERT INTO CLIENTE SET run='{}', nombre='{}', apellido='{}', direccion='{}',"\
            "fono={}, correo='{}', montoCredito={}, deuda={}," \
            "TIPO_id={}".format(c.run, c.nombre, c.apellido, c.direccion, c.fono, c.correo, c.montoCredito, c.deuda, c.tipo)
        con.ejecuta_query(sql)
        con.commit()
        input("\n\n Datos Ingresados Satisfactoriamente")
        con.desconectar()
    except Exception as e:
        print(e)
        system("pause")

def editar(c):
    try:
        con = Conexion(host, user, password, db)
        sql = "UPDATE CLIENTE SET run='{}', nombre='{}', apellido='{}', direccion='{}', fono={}, correo='{}',"\
            "montoCredito={}, deuda={}, TIPO_id={} WHERE id = {}".format(c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[0])
        con.ejecuta_query(sql)
        con.commit()
        input("\n\n Datos Modificados Satisfactoriamente")
        con.desconectar()
    except Exception as e:
        print(e)
        system("pause")

def eliminar(id):
    try:
        con = Conexion(host, user, password, db)
        sql = "DELETE FROM CLIENTE WHERE id = {}".format(id)
        con.ejecuta_query(sql)
        con.commit()
        input("\n\n Cliente Eliminado Satisfactoriamente")
        con.desconectar()
    except Exception as e:
        print(e)
        system("pause")

def mostrartodos():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM CLIENTE"
        cursor = con.ejecuta_query(sql)
        datos = cursor.fetchall()
        con.desconectar()
        return datos
    except Exception as e:
        print(e)
        system("pause")

def consultaparticular(id):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM CLIENTE WHERE id = {}".format(id)
        cursor = con.ejecuta_query(sql)
        datos = cursor.fetchone()
        con.desconectar()
        return datos
    except Exception as e:
        print(e)
        system("pause")

def consultaparcial(cant):
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT * FROM CLIENTE"
        cursor = con.ejecuta_query(sql)
        datos = cursor.fetchmany(size=cant)
        con.desconectar()
        return datos
    except Exception as e:
        con.rollback()
        print(e)
        system("pause")

def mostrartipos():
    try:
        con = Conexion(host, user, password, db)
        sql = "SELECT id, nombre FROM TIPO"
        cursor = con.ejecuta_query(sql)
        datos = cursor.fetchall()
        con.desconectar()
        return datos
    except Exception as e:
        con.rollback()
        print(e)
        system("pause")