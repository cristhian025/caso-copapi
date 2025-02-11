class Predeterminado:
    # Configuraciones base
    SECRET_KEY = 'esta_es_una_clave_extremadamente_dificil'
    # Configuraciones comunes que podrían ser extendidas o sobreescritas por configuraciones específicas

class Local:
    #Configuraciones para bd
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'copapi_db'
    
class Produccion(Predeterminado):
    #Configuraciones para bd
    MYSQL_HOST = 'link_host'
    MYSQL_USER = 'usuario'
    MYSQL_PASSWORD = 'password_asignado'
    MYSQL_DB = 'nombre_de_la_bd'

class ConfigDesarrollo(Predeterminado,Local):
    #Configuraciones específicas para el entorno de desarrollo
    DEBUG = True