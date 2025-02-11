from database.db import conectar_bd
from utils.mensaje_error import formato_error
from utils.formato_time import fecha,fecha_hora
        
class ReporteModel():

    @staticmethod
    def reporte_materiales_ingresados(fecha_inicio,fecha_fin,estado):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    if estado == '':
                        estado = None
                    cursor.execute('CALL ReporteMaterialesIngresados(%s, %s, %s);',(fecha_inicio,fecha_fin,estado))
                    datos = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'fecha_programada': fecha(fila[0]),
                                'registro_ingreso': fecha_hora(fila[1]) if fila[1] is not None else '',
                                'estado_ingreso': fila[2],
                                'observacion': fila[3],
                                'encargado': fila[4],
                                'deposito': fila[5],
                                'material': fila[6],
                                'cantidad_material': fila[7]
                            }
                            for fila in datos
                        ]
                    }
        except Exception as ex:
            print(f"Error al generar reporte de materiales ingresados, error: {ex}")
            return {'registros': []}
    
    @staticmethod
    def reporte_materiales_enviados(fecha_inicio, fecha_fin, estado, minimo_material_total):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    if estado == '':
                        estado = None
                    cursor.execute('CALL ReporteMaterialesEnviados(%s, %s, %s, %s);',
                                (fecha_inicio, fecha_fin, estado, minimo_material_total))
                    datos = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'proyecto': fila[0],
                                'salida_programada': fecha(fila[1]),
                                'registro_salida': fecha_hora(fila[2]) if fila[2] is not None else '',
                                'estado_transporte': fila[3],
                                'tipo_material': fila[4],
                                'material': fila[5],
                                'total_material': fila[6]
                            }
                            for fila in datos
                        ]
                    }
        except Exception as ex:
            print(f"Error al generar reporte de materiales enviados, error: {ex}")
            return {'registros': []}
        
    @staticmethod
    def reporte_stock(p_deposito, p_tipo_material):
        try:
            with conectar_bd() as conn:
                with conn.cursor() as cursor:
                    cursor.execute('CALL ReporteStock(%s, %s);', (p_deposito, p_tipo_material))
                    datos = cursor.fetchall()
                    return {
                        'registros': [
                            {
                                'deposito': fila[0],
                                'tipo_material': fila[1],
                                'material': fila[2],
                                'descripcion': fila[3],
                                'cantidad_material': fila[4]
                            }
                            for fila in datos
                        ]
                    }
        except Exception as ex:
            print(f"Error al generar reporte de stock, error: {ex}")
            return {'registros': []}