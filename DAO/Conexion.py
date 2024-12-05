import pymysql

class Conexion:
    def __init__(self, host, user, password, db):
        self.db = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db = db
        )
        self.cursor = self.db.cursor()


    def ejecuta_query(self, sql):
        self.cursor.execute(sql)
        return self.cursor
    # def ejecuta_query(self, sql, params=None):
    #     try:
    #         if params:
    #             self.cursor.execute(sql, params)  # Usar los parámetros para consultas seguras
    #         else:
    #             self.cursor.execute(sql)
    #     except Exception as e:
    #         print(f"Error al ejecutar la consulta: {e}")
    #         raise

    def desconectar(self):
        self.db.close()

    def commit(self):
        self.db.commit()

    def rolback(self):
        self.db.rollback()

    def obtenerUsuario(self, username):
        try:
            sql = f"SELECT * FROM usuarios WHERE username ='{username}'"
            cursor=self.ejecuta_query(sql)
            datos=cursor.fetchall()
            return datos
        except Exception as e:
            print(e)
    
    def agregarUsuario(self, username, password_hash, nombre, apellidos, email, tipo_usuario):
        try:
            sql= f"INSERT INTO usuarios (username, password_hash, nombre, apellidos, email, tipo_usuario) " \
                f"VALUES ('{username}','{password_hash}','{nombre}','{apellidos}','{email}','{tipo_usuario}')"
            self.ejecuta_query(sql)
            self.commit()
            return True
        except Exception as e:
            print(f"Error al ejecutar la consulta. Error: {e} ")
            self.rollback()
            return False
        
    def agregarIndicador(self, indicador, fecha_registro, usuario, sitio_proveedor, fecha_consulta):
        # Consulta parametrizada para evitar inyección SQL
        sql = f"INSERT INTO consultas_indicadores" \
            f"(indicador, fecha_registro, fecha_consulta, usuario, sitio_proveedor) " \
            f"VALUES ('{indicador}','{fecha_registro}','{fecha_consulta}','{usuario}','{sitio_proveedor}')"
        
        self.ejecuta_query(sql)
        self.commit()
        return True

    
    

            