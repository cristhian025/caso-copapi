from database.db import conectar_bd
from utils.mensaje_error import formato_error
from utils.formato_time import fecha
        
class TransporteModel():

    @classmethod
    def registrar_transporte(cls,tra,lista_materiales):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    if not lista_materiales:
                        return [False,"La lista de materiales esta vacia!"]
                    else:
                        for materiales in lista_materiales:
                            # Select de verificacion de Stock si cuenta con el material suficiente de abastecimiento
                            verificar= cursor.execute('''SELECT s.id_deposito, s.id_material, s.cantidad_material
                                FROM stock s WHERE s.id_deposito = %s and s.id_material = %s AND s.cantidad_material >= %s;''',
                                (int(materiales['id_deposito']),int(materiales['id_material']),int(materiales['cantidad'])))
                            if not verificar:
                                return [False, "Revise la lista de materiales"]
                                            
                    cursor.execute('''INSERT INTO Transporte (fecha_salida, fecha_hora_registro, observacion, 
                    estado, id_proyecto, placa_vehiculo, id_chofer, id_encargado_deposito) VALUES
                    (%s,NULL,NULL, 'A',%s,NULL, NULL,NULL);''',(tra.fecha_salida, tra.id_proyecto))
                    id_transporte = cursor.lastrowid

                    for materiales in lista_materiales:
                        cursor.execute('''INSERT INTO Detalle_transporte (id_transporte, id_deposito, id_material, cantidad_material) VALUES (%s, %s, %s, %s);''',
                        (id_transporte, int(materiales['id_deposito']),int(materiales['id_material']),int(materiales['cantidad']) ))
                    conn.commit()
                    return [True, 'Registro exitoso!']
        except Exception as ex:
            print(f"Error al registrar transporte: {ex}")
            error = formato_error(ex)
            return [False, error]
    
    @classmethod
    def registrar_recepcion_transporte(cls,recep_tra,transporte):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                if transporte.estado == 'E':
                    cursor.execute('''INSERT INTO Recepcion_transporte (fechahora_entrega, observacion, id_encargado_recepcion, id_transporte) 
                    VALUES (NOW(),%s,%s,%s);''',(recep_tra.observacion, recep_tra.id_encargado_recepcion, recep_tra.id_transporte))
                cursor.execute('''UPDATE Transporte t SET t.estado = %s WHERE t.id = %s;''',
                               (transporte.estado, transporte.id))
                conn.commit()
            conn.close()
            return [True, 'Registro exitoso!']
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
    
    
    @staticmethod
    def obtener_stock(pagina=1, por_pagina=10, busqueda='') -> dict:
        try:
            offset = (pagina - 1) * por_pagina  # Cálculo para la paginación
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    # Consulta con búsqueda y paginación
                    cursor.execute('''
                        SELECT st.id_deposito as id_deposito, st.id_material as id_material, m.nombre as material, 
                            tm.nombre as tipo_material, d.nombre as deposito, st.cantidad_material as cantidad_material
                        FROM stock st
                        JOIN deposito d ON st.id_deposito = d.id
                        JOIN material m ON st.id_material = m.id
                        JOIN tipo_material tm ON m.id_tipo_material = tm.id
                        WHERE m.estado = 'A' AND st.cantidad_material >= 1 AND (m.nombre LIKE %s OR d.nombre LIKE %s)
                        ORDER BY st.id_deposito DESC
                        LIMIT %s OFFSET %s;
                    ''', (f'{busqueda}%', f'{busqueda}%', por_pagina, offset))

                    # Obtener los datos
                    stock = cursor.fetchall()

                    # Consulta para contar el total de registros que coinciden con la búsqueda
                    cursor.execute('''
                        SELECT COUNT(st.id_deposito)
                        FROM stock st
                        JOIN deposito d ON st.id_deposito = d.id
                        JOIN material m ON st.id_material = m.id
                        JOIN tipo_material tm ON m.id_tipo_material = tm.id
                        WHERE m.estado = 'A' AND st.cantidad_material >= 1 AND (m.nombre LIKE %s OR d.nombre LIKE %s);
                    ''', (f'{busqueda}%', f'{busqueda}%'))
                    
                    # Total de registros
                    total_registros = cursor.fetchone()[0]

                    # Retornar los datos con la estructura solicitada
                    return {
                        'registros': [
                            {
                                'id_deposito': fila[0],
                                'id_material': fila[1],
                                'material': fila[2],
                                'tipo_material': fila[3],
                                'deposito': fila[4],
                                'cantidad_material': fila[5]
                            }
                            for fila in stock
                        ],
                        'total_registros': total_registros
                    }

        except Exception as ex:
            print(f"Error al obtener stock: {ex}")
            return {'registros': [], 'total_registros': 0}
    
    @staticmethod
    def obtener_proyectos_transporte_salida(pagina=1, por_pagina=10, busqueda='') -> dict:
        try:
            offset = (pagina - 1) * por_pagina  # Cálculo para la paginación

            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    # Consulta con búsqueda y paginación
                    cursor.execute("""
                        SELECT p.id AS id_proyecto, p.nombre, p.fecha_inicio, p.estado, b.nombre AS barrio,
                            COUNT(t.id_proyecto) AS cantidad_transporte
                        FROM proyecto p
                        JOIN barrio b ON p.id_barrio = b.id
                        JOIN transporte t ON t.id_proyecto = p.id
                        WHERE p.estado = 'A' 
                            AND t.estado = 'A' 
                            AND t.fecha_hora_registro IS NOT NULL
                            AND (p.nombre LIKE %s OR b.nombre LIKE %s)
                        GROUP BY p.id 
                        ORDER BY p.id DESC
                        LIMIT %s OFFSET %s;
                    """, (f'{busqueda}%', f'{busqueda}%', por_pagina, offset))

                    # Obtener los datos
                    proyectos = cursor.fetchall()

                    # Consulta para contar el total de registros que coinciden con la búsqueda
                    cursor.execute("""
                        SELECT COUNT(p.id)
                        FROM proyecto p
                        JOIN barrio b ON p.id_barrio = b.id
                        JOIN transporte t ON t.id_proyecto = p.id
                        WHERE p.estado = 'A' 
                            AND t.estado = 'A' 
                            AND t.fecha_hora_registro IS NOT NULL
                            AND (p.nombre LIKE %s OR b.nombre LIKE %s);
                    """, (f'{busqueda}%', f'{busqueda}%'))

                    # Total de registros
                    total_registros = cursor.fetchone()[0]

                    # Retornar los datos con la estructura solicitada
                    return {
                        'registros': [
                            {
                                'id_proyecto': fila[0],
                                'nombre': fila[1],
                                'fecha_inicio': fecha(fila[2]),  # Convertir fecha
                                'estado': fila[3],
                                'barrio': fila[4],
                                'cantidad_transporte': fila[5]
                            }
                            for fila in proyectos
                        ],
                        'total_registros': total_registros
                    }

        except Exception as ex:
            print(f"Error al obtener proyectos de transporte salida: {ex}")
            return {'registros': [], 'total_registros': 0}
    
    @staticmethod
    def obtener_transportes_proyecto_recepcion(id_proyecto):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''SELECT t.id, t.fecha_salida, t.observacion, v.placa, CONCAT(pl.nombres,' ',pl.p_apellido ) as chofer
                    FROM transporte t
                    JOIN proyecto p ON t.id_proyecto = p.id
                    JOIN vehiculo v ON t.placa_vehiculo = v.placa
                    JOIN chofer ch ON t.id_chofer = ch.id
                    JOIN personal pl ON ch.id = pl.id
                    WHERE t.estado = 'A' AND p.id = %s;''',[id_proyecto])
                    datos = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'id': fila[0],
                                'fecha_salida': fecha(fila[1]),
                                'observacion': fila[2],
                                'placa': fila[3],
                                'chofer': fila[4]
                            }
                            for fila in datos
                        ]
                    }
        except Exception as ex:
            print(f"Error al obtener transportes de proyecto con id:{id}, error: {ex}")
            return {'registros': []}
    
    @staticmethod
    def obtener_detalles_transporte(id_transporte):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''SELECT dt.id_transporte, d.nombre, m.nombre, dt.cantidad_material
                    FROM transporte t 
                    JOIN detalle_transporte dt ON dt.id_transporte = t.id
                    JOIN deposito d ON dt.id_deposito = d.id
                    JOIN material m ON dt.id_material = m.id
                    WHERE dt.id_transporte = %s;''',[id_transporte])
                    datos = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'id': fila[0],
                                'deposito': fila[1],
                                'material': fila[2],
                                'cantidad_material': fila[3]
                            }
                            for fila in datos
                        ]
                    }
        except Exception as ex:
            print(f"Error al obtener detalle de transporte con id:{id}, error: {ex}")
            return {'registros': []}
    
    # ------------------------------- Transporte salida -------------------------------------
    @classmethod
    def registrar_salida_transporte(cls,tra):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:                                      
                    cursor.execute('''UPDATE Transporte t SET t.fecha_hora_registro = NOW(), t.observacion = %s, 
                               t.placa_vehiculo = %s, t.id_chofer = %s, t.id_encargado_deposito = %s WHERE t.id = %s;''',
                               (tra.observacion, tra.placa_vehiculo,tra.id_chofer, tra.id_encargado_deposito, tra.id))
                    conn.commit()
                    return [True, 'Registro exitoso!']
        except Exception as ex:
            print(f"Error al registrar salida transporte: {ex}")
            error = formato_error(ex)
            return [False, error]
        
    @staticmethod
    def obtener_proyectos_disponibles_salida(pagina=1, por_pagina=10, busqueda='') -> dict:
        try:
            offset = (pagina - 1) * por_pagina  # Cálculo para la paginación
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    # Consulta con búsqueda y paginación
                    cursor.execute("""
                        SELECT p.id AS id_proyecto, p.nombre, p.fecha_inicio, p.estado, b.nombre AS barrio,
                            COUNT(t.id_proyecto) AS cantidad_transporte
                        FROM proyecto p
                        JOIN barrio b ON p.id_barrio = b.id
                        JOIN transporte t ON t.id_proyecto = p.id
                        WHERE p.estado = 'A' 
                            AND t.estado = 'A' 
                            AND t.fecha_hora_registro IS NULL
                            AND (p.nombre LIKE %s OR b.nombre LIKE %s)
                        GROUP BY p.id 
                        ORDER BY p.id DESC
                        LIMIT %s OFFSET %s;
                    """, (f'{busqueda}%', f'{busqueda}%', por_pagina, offset))

                    # Obtener los datos
                    proyectos = cursor.fetchall()

                    # Consulta para contar el total de registros que coinciden con la búsqueda
                    cursor.execute("""
                        SELECT COUNT(p.id)
                        FROM proyecto p
                        JOIN barrio b ON p.id_barrio = b.id
                        JOIN transporte t ON t.id_proyecto = p.id
                        WHERE p.estado = 'A' 
                            AND t.estado = 'A' 
                            AND t.fecha_hora_registro IS NULL
                            AND (p.nombre LIKE %s OR b.nombre LIKE %s);
                    """, (f'{busqueda}%', f'{busqueda}%'))
                    total_registros = cursor.fetchone()[0]
                    return {
                        'registros': [
                            {
                                'id_proyecto': fila[0],
                                'nombre': fila[1],
                                'fecha_inicio': fecha(fila[2]),  # Convertir fecha
                                'estado': fila[3],
                                'barrio': fila[4],
                                'cantidad_transporte': fila[5]
                            }
                            for fila in proyectos
                        ],
                        'total_registros': total_registros
                    }
        except Exception as ex:
            print(f"Error al obtener proyectos de disponibles para salida transporte: {ex}")
            return {'registros': [], 'total_registros': 0}
        
    def obtener_vehiculos_disponibles_salida_transporte():
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''SELECT v.placa, v.tipo_vehiculo, CONCAT(mm.modelo, '-', mm.marca) AS modelo_marca
                    FROM vehiculo v
                    JOIN modelo_marca mm ON mm.id = v.id_modelo_marca
                    LEFT JOIN transporte t ON t.placa_vehiculo = v.placa AND t.estado = 'A'
                    WHERE t.placa_vehiculo IS NULL
                    GROUP BY v.placa, v.tipo_vehiculo, modelo_marca;''')
                    datos = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'id': fila[0],
                                'nombre': fila[1] +"-"+ fila[2]
                            }
                            for fila in datos
                        ]
                    }
        except Exception as ex:
            print(f"Error al obtener vehiculos disponibles para salida salida de tranpsporte, error: {ex}")
            return {'registros': []}
        
    def obtener_choferes_disponibles_salida_transporte():
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''SELECT ch.id, p.nombres, p.p_apellido
                    FROM chofer ch
                    JOIN personal p ON p.id = ch.id
                    LEFT JOIN transporte t ON t.id_chofer = ch.id AND t.estado = 'A'
                    WHERE ch.estado = 'A' AND t.placa_vehiculo IS NULL
                    GROUP BY ch.id;''')
                    datos = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'id': fila[0],
                                'nombre': fila[1]+ "-" +fila[2]
                            }
                            for fila in datos
                        ]
                    }
        except Exception as ex:
            print(f"Error al obtener choferes disponibles para salida salida de tranpsporte, error: {ex}")
            return {'registros': []}
        
    def obtener_transportes_proyecto_salida(id_proyecto):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('''SELECT t.id, p.nombre, t.fecha_salida FROM transporte t JOIN proyecto p ON t.id_proyecto = p.id 
                        WHERE t.id_proyecto = %s AND t.fecha_hora_registro IS NULL;''',[id_proyecto])
                    datos = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'id': fila[0],
                                'proyecto': fila[1],
                                'fecha_salida': fecha(fila[2])
                            }
                            for fila in datos
                        ]
                    }
        except Exception as ex:
            print(f"Error al obtener transportes de proyecto para salida con id_proyecto:{id}, error: {ex}")
            return {'registros': []}
        