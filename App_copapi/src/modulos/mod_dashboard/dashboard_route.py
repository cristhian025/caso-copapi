from flask import Blueprint, render_template, request, jsonify
from ..mod_reporte.reporte_model import ReporteModel  # Importamos la clase ReporteModel
from datetime import datetime, timedelta

rt_dashboard = Blueprint('dashboard_bp', __name__, template_folder='templates')

@rt_dashboard.route('/', methods=['GET'])
def inicio_dashboard():
    return render_template('dashboard.html')

@rt_dashboard.route('/reportes/materiales_ingresados', methods=['GET'])
def get_materiales_ingresados():
    fecha_actual = datetime.now()
    fecha_inicio = request.args.get('fecha_inicio', (fecha_actual.replace(month=1, day=1) - timedelta(days=365)).strftime('%Y-%m-%d'))
    fecha_fin = request.args.get('fecha_fin', fecha_actual.strftime('%Y-%m-%d'))
    estado = request.args.get('estado', '')
    datos = ReporteModel.reporte_materiales_ingresados(fecha_inicio, fecha_fin, estado)

    return jsonify(datos)

@rt_dashboard.route('/reportes/materiales_enviados', methods=['GET'])
def get_materiales_enviados():
    fecha_actual = datetime.now()
    fecha_inicio = request.args.get('fecha_inicio', (fecha_actual.replace(month=1, day=1) - timedelta(days=365)).strftime('%Y-%m-%d'))
    fecha_fin = request.args.get('fecha_fin', fecha_actual.strftime('%Y-%m-%d'))
    estado = request.args.get('estado', '')
    minimo_material_total = request.args.get('minimo_material_total', 0)
    datos = ReporteModel.reporte_materiales_enviados(fecha_inicio, fecha_fin, estado, minimo_material_total)
    return jsonify(datos)

@rt_dashboard.route('/reportes/stock', methods=['GET'])
def get_stock():
    deposito = request.args.get('deposito', '')
    tipo_material = request.args.get('tipo_material', '')

    datos = ReporteModel.reporte_stock(deposito, tipo_material)
    return jsonify(datos)
