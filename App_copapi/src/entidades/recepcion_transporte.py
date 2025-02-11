class RecepcionTransporte:
    def __init__(self, id=None, fechahora_entrega=None, observacion=None, id_encargado_recepcion=None, id_transporte=None):
        self.id = id
        self.fechahora_entrega = fechahora_entrega
        self.observacion = observacion
        self.id_encargado_recepcion = id_encargado_recepcion
        self.id_transporte = id_transporte
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'fechahora_entrega': self.fechahora_entrega,
            'observacion': self.observacion,
            'id_encargado_recepcion': self.id_encargado_recepcion,
            'id_transporte': self.id_transporte
        }
