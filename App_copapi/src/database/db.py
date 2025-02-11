from flask import session
from flask_mysqldb import MySQL    

def conectar_bd():
    try:
        if 'sesion_abierta' in session:
            conexion = MySQL().connect
            cursor = conexion.cursor()
            nombre_personal = session['datos_usuario']['nombres']
            rol_personal = session['datos_usuario']['rol']
            cursor.execute("SET @nombre_personal = %s;", (nombre_personal,))
            cursor.execute("SET @rol_personal = %s;", (rol_personal,))
            conexion.commit()
            return conexion
        else:
            return MySQL().connect
    except Exception as ex:
        # En caso de que algo falle en la conexion se envia esta exception
        # Si llega a fallar la conexion revisa las config de la BD
        raise Exception("Error al conectar con la base de datos", ex)
