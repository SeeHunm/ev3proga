from getpass import getpass
import os
import DAO.CRUDCliente
import mysql.connector
import json, requests
from DTO.Cliente import Cliente
from datetime import datetime
from DTO.Usuario import Usuario
from DTO.Indicador import registrar_consulta

url = ""
usuario1 = ""

def menuprincipal():
    os.system('cls')
    print("""
            ================================
                M E N Ú  P R I N C I P A L
            ================================
                    1.- (C) INGRESAR
                    2.- (R) MOSTRAR
                    3.- (U) MODIFICAR
                    4.- (D) ELIMINAR
                    5.- (I) CONSULTAR INDICADORES
                    7.- (E) Salir
            ================================""")
    
def menuUsuarios():
    os.system("cls")
    print("====================================")
    print("      M E N Ú  U S U A R I O S      ")
    print("====================================")
    print("         1.- Iniciar sesión         ")
    print("         2.- Registrar usuario      ")
    print("         3.- Salir                  ")
    print("====================================")

def mostrartodo():
    os.system('cls')
    print("""
            ================================
            MUESTRA DE TODOS LOS CLIENTES
            ================================""")
    datos = DAO.CRUDCliente.mostrartodos()
    for dato in datos:
        print("ID: {} - RUN: {} - NOMBRE: {} - APELLIDO: {} - DIRECCIÓN: {} - FONO: {} - CORREO: {} - MONTO CRÉDITO: {} - DEUDA: {} - TIPO: {}".format(
        dato[0],dato[1],dato[2],dato[3],dato[4],dato[5],dato[6],dato[7],dato[8],dato[9]))
        print("-------------------------------------------------------------------------------------------------------------------------------------")

def menu_indicadores():
    while True:
        print("============================")
        print(" M e n u  p r i n c i p a l ")
        print("============================")
        print(" 1.- Desea consultar los indicadores económicos ")
        print(" 2.- Si desea salir")
        resp = int(input(""))
        if resp == 1:
            print("************** CONSULTA INDICADORES ECONÓMICOS **********")
            print(" UF ")
            print(" IVP ")
            print(" IPC ")
            print(" UTM")
            print(" Dolar ")
            print(" Euro ")
            print("********************************************************")
            indicador = str(input("Ingrese el indicador que desea consultar: ")).lower()       
            fechas = input("Indique la fecha que desea consultar: ")
            fecha(indicador,fechas, usuario1)




def fecha(indicador,fecha, usuario1):
        
        Indicadores_validos= ['uf','ivp','ipc','utm','dolar','euro']
        if indicador.lower() not in Indicadores_validos:
            print("Datos ingresados de manera incorrecta del indicador")
            return
        
        try:
            datetime.strptime(fecha, "%d-%m-%Y")
        except ValueError:
            print("Datos ingresados de manera incorrecta de la fecha")
            return

        url = f"https://mindicador.cl/api/{indicador}/{fecha}"
        url2 = requests.get(url)
        text = url2.text
        datos = json.loads(text)
        for clave, valor in datos.items():
            if clave == 'serie':
                print(f"El valor de {indicador} para el día {fecha} es de ${valor[0]['valor']}")
                print("""==================================DESEA GUARDAR SU CONSULTA[SI/NO]==================================""")
                cons = input(" ")
                if cons == "si":
                    registrar_consulta(indicador,fecha,usuario1,url)
                elif cons == 2:
                    return
        try:
            response = requests.get(url2)
            if response.status_code != 200:
                print(f"Error al obtener datos para la fecha {fecha}: {response.status_code}")
                print(f"Mensaje de la API: {response.text}")
                return
        
            datos = json.loads(response.text)
            if 'serie' in datos and datos['serie']:
                valor_uf = datos['serie'][0]['valor'] if datos['serie'] else None
                if valor_uf:
                    valor_uf = float(valor_uf)
                   
                    return round(valor_uf, 2)  
                else:
                    print(f"No hay datos para la fecha {fecha}")
                    return None
            else:
                print(f"No se encontraron datos en la respuesta para la fecha {fecha}")
                return None
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            print("")

def mostraruno():
    os.system('cls')
    print("""
            ================================
                MUESTRA DE DATOS PARTICULAR
            ================================""")
    op = int(input("\n Ingrese valor de ID del Cliente que desea Mostrar los Datos: "))
    datos = DAO.CRUDCliente.consultaparticular(op)
    print("""
            ================================
                MUESTRA DE DATOS DEL CLIENTE
            ================================
            ID              : {}
            RUN             : {}
            NOMBRE          : {}
            APELLIDO        : {}
            DIRECCIÓN       : {}
            FONO            : {}
            CORREO          : {}
            TIPO            : {}
            MONTO CRÉDITO   : {}
            DEUDA           : {}
            --------------------------------
            """.format(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7],datos[8],datos[9]))
    input("\n\n PRESIONE ENTER PARA CONTINUAR")

def menumostrar():
    os.system('cls')
    print("""
            ================================
                M E N Ú  M O S T R A R
            ================================
                    1.- MOSTRAR TODO
                    2.- MOSTRAR UNO
                    3.- MOSTRAR PARCIAL
                    4.- VOLVER
            ================================""")
    
def mostrarparcial():
    os.system('cls')
    print("""
            ===================================
                MUESTRA PARCIALMENTE LOS CLIENTES
            ===================================""")
    cant = int(input("\nIngrese la Cantidad de Clientes a Mostrar: "))
    datos = DAO.CRUDCliente.consultaparcial(cant)
    for dato in datos:
        print("ID: {} - RUN: {} - NOMBRE: {} - APELLIDO: {} - DIRECCIÓN: {} - FONO: {} - CORREO: {} - MONTO CRÉDITO: {} - DEUDA: {} - TIPO: {}".format(
        dato[0],dato[1],dato[2],dato[3],dato[4],dato[5],dato[6],dato[7],dato[8],dato[9]))
        print("-------------------------------------------------------------------------------------------------------------------------------------")
    input("\n\n PRESIONE ENTER PARA CONTINUAR")
def mostrar():
    while(True):
        menumostrar()
        op2 = int(input("   INGRESE OPCIÓN: "))
        if op2 == 1:
            mostrartodo()
            input("\n\n PRESIONE ENTER PARA CONTINUAR")
        elif op2 == 2:
            mostraruno()
        elif op2 == 3:
            mostrarparcial()
        elif op2 == 4:
            break
        else:
            print("Opción Fuera de Rango")

def modificardatos():
    os.system('cls')
    listanuevos=[]
    print("""
            ===================================
                MÓDULO MODIFICAR CLIENTE
            ===================================""")
    mostrartodo()
    mod = int(input("Ingrese valor de ID del Cliente que desea Modificar: "))
    datos = DAO.CRUDCliente.consultaparticular(mod)

    print("ID              : {}".format(datos[0]))
    listanuevos.append(datos[0])
    print("RUN             : {}".format(datos[1]))
    listanuevos.append(datos[1])
    opm = input("DESEA MODIFICAR EL NOMBRE: {} - [SI/NO] ".format(datos[2]))
    if opm.lower() == "si":
        nombrenuevo = input("INGRESE NOMBRE: ")
        listanuevos.append(nombrenuevo)
    else:
        listanuevos.append(datos[2])
    opm = input("DESEA MODIFICAR EL APELLIDO: {} - [SI/NO] ".format(datos[3]))
    if opm.lower() == "si":
        apellidonuevo = input("INGRESE APELLIDO: ")
        listanuevos.append(apellidonuevo)
    else:
        listanuevos.append(datos[3])
    opm = input("DESEA MODIFICAR LA DIRECCIÓN: {} - [SI/NO] ".format(datos[4]))
    if opm.lower() == "si":
        direcnueva = input("INGRESE DIRECCIÓN: ")
        listanuevos.append(direcnueva)
    else:
        listanuevos.append(datos[4])
    opm = input("DESEA MODIFICAR EL TELÉFONO: {} - [SI/NO] ".format(datos[5]))
    if opm.lower() == "si":
        fononuevo = input("INGRESE TELÉFONO: ")
        listanuevos.append(fononuevo)
    else:
        listanuevos.append(datos[5])
    opm = input("DESEA MODIFICAR EL CORREO: {} - [SI/NO] ".format(datos[6]))
    if opm.lower() == "si":
        correonuevo = input("INGRESE EL CORREO: ")
        listanuevos.append(correonuevo)
    else:
        listanuevos.append(datos[6])
    opm = input("DESEA MODIFICAR LA DEUDA: {} - [SI/NO] ".format(datos[8]))
    if opm.lower() == "si":
        deudanuevo = input("INGRESE DEUDA: ")
        listanuevos.append(deudanuevo)
    else:
        listanuevos.append(datos[8])
    opm = input("DESEA MODIFICAR EL MONTO DE CRÉDITO: {} - [SI/NO] ".format(datos[7]))
    if opm.lower() == "si":
        montonuevo = input("INGRESE MONTO DE CRÉDITO: ")
        listanuevos.append(montonuevo)
    else:
        listanuevos.append(datos[7])
    opm = input("DESEA MODIFICAR EL TIPO: {} - [SI/NO] ".format(datos[9]))
    if opm.lower() == "si":
        #recorremos los tipos
        datos = DAO.CRUDCliente.mostrartipos()
        print("-----------------------------------")
        for dato in datos:
            print("CÓDIGO: {} - {}.".format(dato[0], dato[1]))
        print("-----------------------------------")
        tiponuevo = int(input("INGRESE EL TIPO: "))
        listanuevos.append(tiponuevo)
    else:
        listanuevos.append(datos[9])
    DAO.CRUDCliente.editar(listanuevos)

def ingresardatos():
    os.system('cls')
    print("""
            ================================
                INGRESAR DATOS CLIENTE
            ================================""")
    run = input("INGRESE RUN: ")
    nombre = input("INGRESE NOMBRE: ")
    apellido = input("INGRESE APELLIDO: ")
    direccion = input("INGRESE DIRECCION: ")
    fono = input("INGRESE TELEFONO: ")
    correo = input("INGRESE CORREO: ")
    #recorremos los tipos-------------------
    datos = DAO.CRUDCliente.mostrartipos()
    print("-----------------------------------")
    for dato in datos:
        print("CÓDIGO: {} - {}.".format(dato[0], dato[1]))
    print("-----------------------------------")
    tipo = int(input("Ingrese el código del Tipo de Cliente: "))
    monto = int(input("INGRESE MONTO CRÉDITO: "))

    c = Cliente(run, nombre, apellido, direccion, fono, correo, tipo, monto, deuda=0)
    DAO.CRUDCliente.agregar(c)

def eliminardatos():
    os.system('cls')
    print("""
            ===================================
                MÓDULO ELIMINAR CLIENTE
            ===================================""")
    mostrartodo()
    elim = int(input("Ingrese valor de ID del Cliente que desea Eliminar: "))
    DAO.CRUDCliente.eliminar(elim)

def ingresoUsuarios():
    os.system('cls')
    print("=================================")
    print("       INGRESO DE USUARIO       ")
    print("=================================")
    username = input("INGRESE NOMBRE DE USUARIO: ")
    
    # Verificamos que las contraseñas sean iguales
    while True:
        clave1 = getpass("INGRESE PASSWORD   : ")
        clave2 = getpass("REPITA PASSWORD    : ")
        if clave1 == clave2:
            break
    
    nombre = input("INGRESE NOMBRE      : ")
    apellidos = input("INGRESE APELLIDOS   : ")
    correo = input("INGRESE CORREO      : ")
    
    print("--------- TIPOS DE USUARIOS ---------")
    print("    1 para Administrador")
    print("    2 para Vendedor")
    tipo = int(input("----- Ingrese Nº : "))
    print("-------------------------------------")
    
    if tipo == 1:
        tipo = "Administrador"
    else:
        tipo = "Vendedor"
    
    Usuario.registrar_usuario(username, clave1, nombre, apellidos, correo, tipo)
    print("=================================")

while True:
        # ------- PARA EL MENU DE USUARIOS --------
        menuUsuarios()
        opUsu = int(input("      INGRESE OPCIÓN : "))
        if opUsu == 1:
            usuario1 = input("Ingrese nombre de usuario: ")
            clave = getpass("Ingrese password: ")
            usuario = Usuario.login(usuario1, clave)
            if not usuario:
                input("...Usuario No Registrado!")
                print(f"Bienvenido {usuario.nombre.upper()} {usuario.apellidos.upper()}.2232")
            else:
                print(f"Bienvenido {usuario.nombre.upper()} {usuario.apellidos.upper()}.")
                input("...Presiona ENTRAR para ingresar al Menú Principal.")
                menuprincipal()
                op = int(input("   INGRESE OPCIÓN : "))
                if op == 1:
                    ingresardatos()
                elif op == 2:
                    mostrar()
                    menuprincipal()
                elif op == 3:
                    modificardatos()
                if op == 4:
                    eliminardatos()
                if op == 5:
                    menu_indicadores()
                if op == 6:
                    op2 = input("DESEA SALIR [SI/NO] : ")
                    if op2.lower() == "si":
                        exit()
                else:
                    print("Opción fuera de rango")
        elif opUsu == 2:
            ingresoUsuarios()
            input("....Presione Entrar para continuar")
        else:
            opSalir = input("DESEA SALIR [SI/NO] : ")
            if opSalir.lower() == "si":
                exit()




