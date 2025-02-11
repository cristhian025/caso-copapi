from flask import Blueprint, request, render_template, render_template

rt_stock = Blueprint('stock_bp', __name__, template_folder='templates')

@rt_stock.route('/reg_stock', methods=['GET','POST'])
def reg_stock():
    if request.method == 'GET':
        return render_template('reg_stock.html')
    
