from flask import Blueprint, jsonify, request, render_template, url_for, redirect, render_template

# Entidades
from entidades.proyecto import Proyecto
# Modelos
from .proyecto_model import ProyectoModel

rt_proyecto = Blueprint('proyecto_bp', __name__, template_folder='templates')

# ============= Mostrar Proyectos =============
@rt_proyecto.route('/mostrar_proyectos', methods=['GET'])
def mostrar_proyectos():
    return render_template('mostrar_proyectos.html')

@rt_proyecto.route('/obtener_proyectos', methods=['GET'])
def obtener_proyectos():
    try:
        data = request.args
        pagina = int(data.get('pagina', 1))
        por_pagina = int(data.get('por_pagina', 10))
        busqueda = data.get('busqueda', '')
        dato_obtenidos = ProyectoModel.obtener_proyectos(pagina, por_pagina, busqueda)
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500
    
# ============= Modificar o Editar Proyecto =============
@rt_proyecto.route('/modificar_proyecto/<int:id_proyecto>', methods=['GET', 'PUT'])
def modificar_proyecto(id_proyecto):
    if request.method == 'GET':
        try:
            dato_obtenidos=ProyectoModel.obtener_proyecto(id_proyecto)
            return render_template('modificar_proyecto.html', datos=dato_obtenidos)
        except Exception as ex:
            print(ex)
            mensaje = "No se encontro el proyecto!"
            return render_template('error.html', error = mensaje)
    elif request.method == 'PUT':
        try:
            data = request.form
            print(id_proyecto,data.get('nombre'),data.get('estado'))
            ent_proyecto = Proyecto(
                id=id_proyecto,
                nombre=data.get('nombre'),
                estado=data.get('estado')
                )
            resultado = ProyectoModel.modificar_proyecto(ent_proyecto)
            if resultado[0]:
                respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                            'redireccion': '/proyecto/mostrar_proyectos'}
                return jsonify(respuesta)
            else:
                respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
                return jsonify(respuesta)
        except Exception as ex:
            print(ex)
            return jsonify({'error': 'No se pudieron actualizar los datos'}), 500

# ============= Registrar Proyecto =============
@rt_proyecto.route('/obtener_barrios', methods=['GET'])
def obtener_barrios():
    try:
        dato_obtenidos = ProyectoModel.obtener_barrios()
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500
    
@rt_proyecto.route('/obtener_servicios', methods=['GET'])
def obtener_servicios():
    try:
        dato_obtenidos = ProyectoModel.obtener_servicios()
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500
    
@rt_proyecto.route('/reg_proyecto', methods=['GET','POST'])
def reg_proyecto():
    if request.method == 'POST':
        data = request.form
        ent_proyecto = Proyecto(
            nombre=data.get('nombre'),
            fecha_inicio=data.get('fecha_inicio'),
            estado='A',
            id_barrio=data.get('id_barrio')
            )
        id_servicios = data.getlist('id_servicios')
        resultado = ProyectoModel.registrar_proyecto(ent_proyecto,id_servicios)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/proyecto/reg_proyecto'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        return render_template('reg_proyecto.html')

