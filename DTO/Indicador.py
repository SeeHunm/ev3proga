from DTO.SocioNegocio import SocioNegocio
from DTO.Tipo import Tipo_Usuario
import datetime
from DAO.Conexion import Conexion
import bcrypt


host='localhost'
user='userempresa'
passwordS='V3ntana.13'
db='empresa'

class Indicador:
    def __init__(self, indicador, fecha_registro, usuario, sitio_proveedor):
        self.indicador = indicador
        self.fecha_registro = fecha_registro
        self.usuario = usuario
        self.sitio_proveedor = sitio_proveedor
    
def registrar_consulta(indicador, fecha_registro, usuario, sitio_proveedor):
    con = Conexion(host, user, passwordS, db)
    try:
        fecha_consulta = datetime.datetime.now()

        print(f"Datos a registrar: Indicador={indicador}, Fecha Registro={fecha_registro}, Usuario={usuario}, Sitio Proveedor={sitio_proveedor}, Fecha Consulta={fecha_consulta}")

        # Intentar registrar la consulta
        resp = con.agregarIndicador(indicador, fecha_registro, usuario, sitio_proveedor, fecha_consulta)
        if resp:
            print(f"Consulta registrada con éxito: Indicador={indicador}, Fecha Registro={fecha_registro}")
        else:
            print("No se pudo registrar la consulta.")
    except Exception as e:
        print(f"Error al insertar los datos: {e}")  # Mostrar detalles del error
    finally:
        con.desconectar()

# def registrar_consulta(indicador, fecha_registro, usuario, sitio_proveedor):
#         con = Conexion(host, user, passwordS, db)
#         try:
#             fecha_consulta = datetime.now()
#             print(indicador, fecha_registro, usuario, sitio_proveedor, fecha_consulta)

#             resp = con.agregarIndicador(indicador, fecha_registro, usuario, sitio_proveedor, fecha_consulta)
#             if resp:
#                 print(f"Consulta registrada con éxito: {indicador} en {fecha_registro}")
#             else:
#                  print("no pa na")
#         except:
#             print(f"Error al insertar los datos")
#         # finally:
#         #     if conexion:
#         #         conexion.close()