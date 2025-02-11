from database.db import conectar_bd
from utils.mensaje_error import formato_error
from utils.formato_time import fecha
        
class ProyectoModel():

    @classmethod
    def registrar_proyecto(cls,pro,id_servicios):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    # Verificar si el servicio esta activo
                    if not id_servicios:
                        return [False,"El servicio no fue seleccionado"]
                    else:
                        for id_servicio in id_servicios:
                            cursor.execute('''SELECT estado FROM Servicio WHERE id = %s''',(id_servicio,))
                            servicio_estado = cursor.fetchone()
                            if servicio_estado[0] != 'A':
                                return [False,"El servicio no esta activo"]
                    # Insertar en la tabla Proyecto
                    cursor.execute('''INSERT INTO Proyecto (nombre, fecha_inicio, id_barrio, estado) 
                                VALUES (%s, %s, %s, %s)''',(pro.nombre, pro.fecha_inicio, pro.id_barrio,'A'))
                    id_proyecto = cursor.lastrowid

                    # Insertar en la tabla Proyecto_servicio
                    for id_servicio in id_servicios:
                        cursor.execute('''INSERT INTO Proyecto_servicio (id_proyecto, id_servicio) 
                                    VALUES (%s, %s)''',(id_proyecto, id_servicio))
                    conn.commit()
                    return [True, 'Registro exitoso!']
        except Exception as ex:
            print(f"Error al registrar proyecto: {ex}")
            error = formato_error(ex)
            return [False, error]
        
    @classmethod
    def modificar_proyecto(cls, pro):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''UPDATE Proyecto SET nombre = %s, estado =  %s WHERE id = %s;''',(pro.nombre, pro.estado, pro.id))
                    conn.commit()
                    return [True, 'Modificacion exitosa!']
        except Exception as ex:
            print(f"Error al modificar proyecto: {ex}")
            error = formato_error(ex)
            return [False, error]
    
    @staticmethod
    def obtener_proyectos(pagina=1, por_pagina=10, busqueda='') -> dict:
        try:
            offset = (pagina - 1) * por_pagina
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    # Construir consulta para obtener los proyectos con búsqueda y paginación
                    cursor.execute('''
                        SELECT p.id as id_proyecto, p.nombre, p.fecha_inicio, p.fecha_fin, p.estado, 
                            b.nombre, GROUP_CONCAT(s.nombre SEPARATOR ', ') as servicios
                        FROM proyecto p
                        JOIN proyecto_servicio ps ON ps.id_proyecto = p.id
                        JOIN servicio s ON ps.id_servicio = s.id
                        JOIN barrio b ON p.id_barrio = b.id
                        WHERE p.nombre LIKE %s OR b.nombre LIKE %s
                        GROUP BY p.id
                        ORDER BY p.id DESC
                        LIMIT %s OFFSET %s;
                    ''', (f'{busqueda}%', f'{busqueda}%', por_pagina, offset))
                    proyectos = cursor.fetchall()

                    # Consulta para contar el total de registros que coinciden con la búsqueda
                    cursor.execute('''
                        SELECT COUNT(DISTINCT p.id)
                        FROM proyecto p
                        JOIN barrio b ON p.id_barrio = b.id
                        WHERE p.nombre LIKE %s OR b.nombre LIKE %s;
                    ''', (f'{busqueda}%', f'{busqueda}%'))
                    total_registros = cursor.fetchone()[0]

                    return {
                        'registros': [
                            {
                                'id': fila[0],
                                'nombre': fila[1],
                                'fecha_inicio': fecha(fila[2]),
                                'fecha_fin': fecha(fila[3]) if fila[3] is not None else '',
                                'estado': fila[4],
                                'barrio': fila[5],
                                'servicios': fila[6]
                            }
                            for fila in proyectos
                        ],
                        'total_registros': total_registros
                    }
        except Exception as ex:
            print(f"Error al obtener proyectos: {ex}")
            return {'registros': [], 'total_registros': 0}
        
    def obtener_proyecto(id):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""SELECT p.id as id_proyecto, p.nombre, p.fecha_inicio, p.estado, 
                                b.nombre as barrio, GROUP_CONCAT(s.nombre SEPARATOR ', ') as servicios
                    FROM proyecto p
                    JOIN proyecto_servicio ps ON ps.id_proyecto = p.id
                    JOIN servicio s ON ps.id_servicio = s.id
                    JOIN barrio b ON p.id_barrio = b.id
                    WHERE p.id = %s
                    GROUP BY p.id;""",[id])
                    datos = cursor.fetchone()
                    return {
                        'registros': {
                            'id': datos[0],
                            'nombre': datos[1],
                            'fecha_inicio': fecha(datos[2]),
                            'estado': datos[3],
                            'barrio': datos[4],
                            'servicios': datos[5]
                            }
                    }
        except Exception as ex:
            print(f"Error al obtener proyecto con id:{id}, error: {ex}")
            return {'registros': []}
        
    def obtener_barrios():
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""SELECT b.id, b.nombre, b.ubicacion FROM barrio b;""")
                    barrios = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'id': fila[0],
                                'nombre': fila[1] 
                            }
                            for fila in barrios
                        ]
                    }
        except Exception as ex:
            print(f"Error al obtener barrios, error: {ex}")
            return {'registros': []}
    
    def obtener_servicios():
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""SELECT s.id, s.nombre FROM servicio s WHERE s.estado = 'A';""")
                    barrios = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'id': fila[0],
                                'nombre': fila[1] 
                            }
                            for fila in barrios
                        ]
                    }
        except Exception as ex:
            print(f"Error al obtener barrios, error: {ex}")
            return {'registros': []}
        