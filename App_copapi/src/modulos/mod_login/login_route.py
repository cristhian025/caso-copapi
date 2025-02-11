from flask import Blueprint, jsonify, request, session, render_template, url_for, redirect, render_template
# Entidades
from entidades.usuario import Usuario
# Modelos
from .login_model import SesionUsuario

rt_login = Blueprint('login_bp', __name__, template_folder='templates')

@rt_login.route('/', methods=['GET'])
def inicio():
    if 'sesion_abierta' in session:
        if session['datos_id']['id_rol'] == 1:
            return redirect(url_for("dashboard_bp.inicio_dashboard"))
        # agregar a futuro otros acceso para distintos roles
        return render_template('menu.html')
    else:
        return redirect(url_for("login_bp.ingreso_login"))
    
@rt_login.route('/login', methods=['POST', 'GET'])
def ingreso_login():
    if request.method == 'POST':
        data = request.form
        ent_usuario = Usuario(
            usuario = data.get('usuario'),
            password = data.get('password')
        )
        resultado = SesionUsuario.verificar_usuario(ent_usuario)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    if request.method == 'GET':
        return render_template('login.html')

@rt_login.route('/cerrar_sesion')
def cerrar_sesion():
    SesionUsuario.cerrar_sesion()
    return redirect(url_for('login_bp.inicio'))
