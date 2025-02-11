from flask import session
from database.db import conectar_bd
from utils.mensaje_error import formato_error
        
class SesionUsuario():

    @classmethod
    def verificar_usuario(cls, usu):
        try:
            respuesta = [False, 'creedenciales incorrectas!']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute('call verificar_credencial(%s, %s)', (usu.usuario, usu.password))
                resultado_sql = cursor.fetchone()
                if resultado_sql:
                    SesionUsuario.guardar_sesion(resultado_sql)
                    respuesta = [True, 'credenciales correctas!']
            conn.close()
            return respuesta
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
    
    def guardar_sesion(datos):
        session['sesion_abierta'] = True
        #---------------
        session['datos_usuario'] = {
            'nombres': datos[0],
            'apellido_1': datos[1],
            'apellido_2': datos[2] if datos[2] is not None else '',
            'rol': datos[3]
        }
        session['datos_id'] = {
            'id_personal': datos[4],
            'id_usuario': datos[5],
            'id_rol': datos[6]
        }

    def cerrar_sesion():
        session.clear()
