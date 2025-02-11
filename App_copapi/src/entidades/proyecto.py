class Proyecto:
    def __init__(self, id=None, nombre=None, fecha_inicio=None, fecha_fin=None, estado=None, id_barrio=None):
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.id_barrio = id_barrio
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'estado': self.estado,
            'id_barrio': self.id_barrio
        }