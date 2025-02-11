class Transporte:
    def __init__(self, id=None, fecha_salida=None, fecha_hora_registro=None, observacion=None, estado=None,
                 id_proyecto=None, placa_vehiculo=None, id_chofer=None, id_encargado_deposito=None):
        self.id = id
        self.fecha_salida = fecha_salida
        self.fecha_hora_registro = fecha_hora_registro
        self.observacion = observacion
        self.estado = estado
        self.id_proyecto = id_proyecto
        self.placa_vehiculo = placa_vehiculo
        self.id_chofer = id_chofer
        self.id_encargado_deposito = id_encargado_deposito
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'fecha_salida': self.fecha_salida,
            'fecha_hora_registro': self.fecha_hora_registro,
            'observacion': self.observacion,
            'estado': self.estado,
            'id_proyecto': self.id_proyecto,
            'placa_vehiculo': self.placa_vehiculo,
            'id_chofer': self.id_chofer,
            'id_encargado_deposito': self.id_encargado_deposito
        }
