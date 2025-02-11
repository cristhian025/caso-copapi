from flask import Blueprint, request, jsonify, render_template
from utils.generador_reportes import generar_reporte

# Modelos
from .reporte_model import ReporteModel

rt_reporte = Blueprint('reporte_bp', __name__, template_folder='templates')

# ============================== Reporte Materiales Ingresados ==============================
@rt_reporte.route('/materiales_ingresados', methods=['GET'])
def reporte_materiales_ingresados():
    return render_template('materiales_ingresados.html')

@rt_reporte.route('/materiales_ingresados/<formato>', methods=['POST'])
def reporte_materiales_ingresados_descarga(formato):
    try:
        data = request.form
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        estado_ingreso = data.get('estado_ingreso')
        datos = ReporteModel.reporte_materiales_ingresados(fecha_inicio, fecha_fin, estado_ingreso)
        
        columnas = ["fecha_programada", "registro_ingreso", "estado_ingreso", "observacion", "encargado", "deposito", "material", "cantidad_material"]
        titulo_columnas = ["Fecha Programada", "Registro Ingreso", "Estado Ingreso", "Observación", "Encargado", "Deposito", "Material", "Cantidad Material"]

        if formato == "excel":
            return generar_reporte(nombre_reporte="Reporte_Materiales_Ingresados",titulo="",registros= datos['registros'],keys=columnas,formato="excel", headers=titulo_columnas)
        elif formato == "pdf":
            return generar_reporte(nombre_reporte="Reporte_Materiales_Ingresados", titulo="Reporte de Materiales Ingresados a Stock", registros=datos['registros'], 
                                   keys=columnas, formato="pdf", headers=titulo_columnas)
    except Exception as e:
        print(f"Error generando archivo de Reporte de Materiales Ingresados a Stock: {e}")
        return jsonify({"error": "No se pudo generar el archivo"}), 500
    
# ============================== Reporte Materiales Enviados ==============================
@rt_reporte.route('/materiales_enviados', methods=['GET'])
def reporte_materiales_enviados():
    return render_template('materiales_enviados.html')

@rt_reporte.route('/materiales_enviados/<formato>', methods=['POST'])
def reporte_materiales_enviados_descarga(formato):
    try:
        data = request.form
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        estado_transporte = data.get('estado_transporte')
        minimo_material_total = int(data.get('minimo_material_total'))
        datos = ReporteModel.reporte_materiales_enviados(fecha_inicio, fecha_fin, estado_transporte, minimo_material_total)
        
        columnas = ["proyecto", "salida_programada", "registro_salida", "estado_transporte", "tipo_material", "material", "total_material"]
        titulo_columnas = ["Proyecto", "Salida Programada", "Registro Salida", "Estado Transporte", "Tipo Material", "Material", "Total Material"]
        if formato == "excel":
            return generar_reporte(nombre_reporte="Reporte_Materiales_Enviados", titulo="", registros=datos['registros'], keys=columnas, formato="excel", headers=titulo_columnas)
        elif formato == "pdf":
            return generar_reporte(nombre_reporte="Reporte_Materiales_Enviados", titulo="Reporte de Materiales Enviados en Proyectos", registros=datos['registros'], keys=columnas, formato="pdf", headers=titulo_columnas)
    except Exception as e:
        print(f"Error generando archivo de Reporte de Materiales Enviados en Proyectos: {e}")
        return jsonify({"error": "No se pudo generar el archivo"}), 500
    
# ============================== Reporte Stock ==============================
@rt_reporte.route('/reporte_stock', methods=['GET'])
def reporte_stock():
    if request.method == 'GET':
        return render_template('reporte_stock.html')

@rt_reporte.route('/reporte_stock/<formato>', methods=['POST'])
def reporte_stock_descarga(formato):
    try:
        data = request.form
        p_deposito = data.get('p_deposito')
        p_tipo_material = data.get('p_tipo_material')
        datos = ReporteModel.reporte_stock(p_deposito, p_tipo_material)
        
        columnas = ["deposito", "tipo_material", "material", "descripcion", "cantidad_material"]
        titulo_columnas = ["Deposito", "Tipo Material", "Material", "Descripción", "Cantidad Material"]
        if formato == "excel":
            return generar_reporte(nombre_reporte="Reporte_Stock", titulo="", registros=datos['registros'], keys=columnas, formato="excel", headers=titulo_columnas)
        elif formato == "pdf":
            return generar_reporte(nombre_reporte="Reporte_Stock", titulo="Reporte de Stock",registros= datos['registros'], keys=columnas, formato="pdf", headers=titulo_columnas)
    except Exception as e:
        print(f"Error generando archivo de Reporte de Stock: {e}")
        return jsonify({"error": "No se pudo generar el archivo"}), 500