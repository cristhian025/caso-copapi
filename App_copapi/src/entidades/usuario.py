class Usuario:
    def __init__(self, id=None, usuario=None, password=None, estado=None, id_personal=None, id_rol=None):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.estado = estado
        self.id_personal = id_personal
        self.id_rol = id_rol
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'usuario': self.usuario,
            'password': self.password,
            'estado': self.estado,
            'id_personal': self.id_personal,
            'id_rol': self.id_rol
        }