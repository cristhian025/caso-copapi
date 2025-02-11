
def formato_error(resultado):
    # Si resultado es una cadena, regresa la cadena directamente.
    if isinstance(resultado, str):
        return resultado

    # Si es una excepción con atributos 'args', trata de acceder a ellos.
    if isinstance(resultado, Exception):
        if hasattr(resultado, 'args') and len(resultado.args) > 0:
            # Devuelve el mensaje de error completo de la excepción
            return ' '.join(map(str, resultado.args))
        else:
            # Si no hay 'args', regresa la representación string del error.
            return str(resultado)

    # Si resultado no es una excepción o una cadena, trata de convertirlo a string.
    return str(resultado)
