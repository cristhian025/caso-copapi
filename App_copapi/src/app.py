from flask import Flask, render_template
from flask_mysqldb import MySQL
from config.general import ConfigDesarrollo

# rutas de Modulos
from modulos.mod_login.login_route import rt_login
from modulos.mod_proyecto.proyecto_route import rt_proyecto
from modulos.mod_transporte.transporte_route import rt_transporte
from modulos.mod_stock.stock_route import rt_stock
from modulos.mod_reporte.reporte_route import rt_reporte
from modulos.mod_dashboard.dashboard_route import rt_dashboard

app = Flask(__name__)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('Error404.html'), 404

if __name__ == '__main__':
    # cargar configuraciones
    app.config.from_object(ConfigDesarrollo)
    # iniciar la BD
    inicio_mysql = MySQL(app)
    # blueprints
    app.register_blueprint(rt_login, url_prefix='/')
    app.register_blueprint(rt_dashboard, url_prefix='/dashboard')
    app.register_blueprint(rt_proyecto, url_prefix='/proyecto')
    app.register_blueprint(rt_transporte, url_prefix='/transporte')
    app.register_blueprint(rt_stock, url_prefix='/stock')
    app.register_blueprint(rt_reporte, url_prefix='/reporte')
    
    # Ejecutar el servidor
    app.run(port=5020)