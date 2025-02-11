from flask import Blueprint, json, jsonify, request, session, render_template, url_for, redirect, render_template

# Entidades
from entidades.transporte import Transporte
from entidades.recepcion_transporte import RecepcionTransporte
# Modelos
from .transporte_model import TransporteModel

rt_transporte = Blueprint('transporte_bp', __name__, template_folder='templates')

# ============= Registrar Transporte =============
@rt_transporte.route('/reg_transporte', methods=['GET'])
def reg_transporte_fase1():
    return render_template('reg_transporte1.html')

@rt_transporte.route('/reg_transporte/<int:id>',  methods=['GET','POST'])
def reg_transporte_fase2(id):
    if request.method == 'POST':
        data = request.form
        id_proyecto = id
        fecha_salida = data.get('fecha_salida')
        lista_materiales = json.loads(data.get('lista_materiales'))
        ent_tranporte = Transporte(id_proyecto=id_proyecto,fecha_salida=fecha_salida)
        resultado = TransporteModel.registrar_transporte(ent_tranporte,lista_materiales)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/transporte/reg_transporte'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        return render_template('reg_transporte2.html', id_proyecto = id)

@rt_transporte.route('/obtener_stock', methods=['GET'])
def obtener_stock():
    try:
        data = request.args
        pagina = int(data.get('pagina', 1))
        por_pagina = int(data.get('por_pagina', 10))
        busqueda = data.get('busqueda', '')
        dato_obtenidos = TransporteModel.obtener_stock(pagina, por_pagina, busqueda)
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500
    
# ============= Registrar Salida Transporte =============
    
@rt_transporte.route('/reg_salida_transporte', methods=['GET'])
def reg_salida_transporte_fase1():
    return render_template('reg_salida_transporte_fase1.html')

@rt_transporte.route('/reg_salida_transporte/<int:id_proyecto>', methods=['GET','POST'])
def reg_salida_transporte_fase2(id_proyecto):
    if request.method == 'POST':
        data = request.form
        id_transporte = data.get('id_transporte')
        id_chofer = data.get('id_chofer')
        placa_vehiculo = data.get('placa_vehiculo')
        if id_transporte == '' or id_chofer == '' or placa_vehiculo == '':
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':"rellene el formulario correctamente!"}
            return jsonify(respuesta)
        observacion = data.get('observacion')
        id_encargado_deposito = session['datos_id']['id_personal']
        resultado = [False, "prueba"]
        ent_tranporte = Transporte(id=id_transporte, id_chofer=id_chofer, placa_vehiculo=placa_vehiculo,observacion=observacion,id_encargado_deposito=id_encargado_deposito)
        resultado = TransporteModel.registrar_salida_transporte(ent_tranporte)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/transporte/reg_salida_transporte'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        id_proyecto = id_proyecto
        select_vehiculos = TransporteModel.obtener_vehiculos_disponibles_salida_transporte()
        select_choferes = TransporteModel.obtener_choferes_disponibles_salida_transporte()
        return render_template('reg_salida_transporte_fase2.html',id_proyecto=id_proyecto, select_vehiculos=select_vehiculos, select_choferes=select_choferes)

@rt_transporte.route('/obtener_proyectos_disponibles_salida', methods=['GET'])
def obtener_proyectos_disponibles_salida():
    try:
        data = request.args
        pagina = int(data.get('pagina', 1))
        por_pagina = int(data.get('por_pagina', 10))
        busqueda = data.get('busqueda', '')
        dato_obtenidos = TransporteModel.obtener_proyectos_disponibles_salida(pagina, por_pagina, busqueda)
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500
    
@rt_transporte.route('/obtener_vehiculos_disponibles_salida_transporte', methods=['GET'])
def obtener_vehiculos_disponibles_salida_transporte():
    try:
        dato_obtenidos = TransporteModel.obtener_vehiculos_disponibles_salida_transporte()
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500

@rt_transporte.route('/obtener_choferes_disponibles_salida_transporte', methods=['GET'])
def obtener_choferes_disponibles_salida_transporte():
    try:
        dato_obtenidos = TransporteModel.obtener_choferes_disponibles_salida_transporte()
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500

@rt_transporte.route('/obtener_transportes_proyecto_salida/<int:id_proyecto>', methods=['GET'])
def obtener_transportes_proyecto_salida(id_proyecto):
    try:
        dato_obtenidos = TransporteModel.obtener_transportes_proyecto_salida(id_proyecto)
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500
    
# ============= Registrar Recepcion Transporte =============
@rt_transporte.route('/reg_recepcion_transporte', methods=['GET'])
def reg_recepcion_transporte_fase1():
    return render_template('reg_recepcion_transporte1.html')

@rt_transporte.route('/obtener_proyectos_transporte_salida', methods=['GET'])
def obtener_proyectos_transporte_salida():
    try:
        data = request.args
        pagina = int(data.get('pagina', 1))
        por_pagina = int(data.get('por_pagina', 10))
        busqueda = data.get('busqueda', '')
        dato_obtenidos = TransporteModel.obtener_proyectos_transporte_salida(pagina, por_pagina, busqueda)
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500
    
@rt_transporte.route('/reg_recepcion_transporte/<int:id_proyecto>', methods=['GET','POST'])
def reg_recepcion_transporte_fase2(id_proyecto):
    if request.method == 'POST':
        data = request.form
        id_transporte = data.get('id_transporte')
        if id_transporte == '':
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':"seleccione un transporte de proyecto a recepcionar!"}
            return jsonify(respuesta)
        observacion = data.get('observacion'),
        estado_transporte = data.get('estado_transporte')
        id_encargado_recepcion = session['datos_id']['id_personal']
        ent_recep_tranporte = RecepcionTransporte(id_transporte=id_transporte,observacion=observacion,id_encargado_recepcion=id_encargado_recepcion)
        ent_transporte = Transporte(id=id_transporte,estado=estado_transporte)
        resultado = TransporteModel.registrar_recepcion_transporte(ent_recep_tranporte,ent_transporte)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/transporte/reg_recepcion_transporte'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        return render_template('reg_recepcion_transporte2.html',id_proyecto=id_proyecto)

@rt_transporte.route('/obtener_transportes_proyecto_recepcion/<int:id_proyecto>', methods=['GET'])
def obtener_transportes_proyecto_recepcion(id_proyecto):
    try:
        dato_obtenidos = TransporteModel.obtener_transportes_proyecto_recepcion(id_proyecto)
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500

@rt_transporte.route('/obtener_detalles_transporte/<int:id_transporte>', methods=['GET'])
def obtener_detalles_transporte(id_transporte):
    try:
        dato_obtenidos = TransporteModel.obtener_detalles_transporte(id_transporte)
        return jsonify(dato_obtenidos), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500