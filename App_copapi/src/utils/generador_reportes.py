from flask import jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from datetime import datetime
import pandas as pd

NOMBRE_EMPRESA = "COPAPI"
FONDO = "static/imgs/logo.jpg"

def ajustar_ancho_columnas_proporcional(table_data, fontName='Helvetica', fontSize=10, padding=5, gap=5, available_width=1000):
    """
    Calcula el ancho óptimo de cada columna de manera proporcional según el contenido,
    respetando el ancho mínimo (sin escalar hacia arriba) y agregando un espacio (gap)
    fijo entre columnas. Si el total (ancho de columnas + gaps) excede el ancho disponible,
    se escala proporcionalmente hacia abajo.
    
    :param table_data: Lista de filas (listas) con el contenido en texto plano.
    :param fontName: Fuente para medir el ancho.
    :param fontSize: Tamaño de la fuente.
    :param padding: Espacio interno (a cada lado) que se suma al ancho del texto.
    :param gap: Espacio deseado entre columnas.
    :param available_width: Ancho total disponible para la tabla.
    :return: Tuple (widths, gap) donde widths es una lista con el ancho de cada columna.
    """
    num_cols = len(table_data[0])
    widths = [0] * num_cols
    for row in table_data:
        for i, cell in enumerate(row):
            cell_width = pdfmetrics.stringWidth(str(cell), fontName, fontSize) + 2 * padding
            widths[i] = max(widths[i], cell_width)
    
    total_needed = sum(widths) + gap * (num_cols - 1)
    
    # Solo escalamos hacia abajo si el total excede el ancho disponible.
    if total_needed > available_width:
        factor = available_width / total_needed
        widths = [w * factor for w in widths]
        gap = gap * factor

    return widths, gap

# Canvas personalizado para agregar marca de agua (watermark) semi-transparente
class WatermarkCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.fondo_imagen = kwargs.pop('fondo_imagen', None)
        super(WatermarkCanvas, self).__init__(*args, **kwargs)
    
    def draw_watermark(self):
        if self.fondo_imagen:
            self.saveState()
            try:
                self.setFillAlpha(0.2)  # 20% opaco
            except AttributeError:
                # Si la versión de ReportLab no soporta setFillAlpha
                pass
            page_width, page_height = self._pagesize
            image_width = 300  # Ajusta según necesites
            image_height = 300
            x = (page_width - image_width) / 2
            y = (page_height - image_height) / 2
            self.drawImage(self.fondo_imagen, x, y, width=image_width, height=image_height, mask='auto')
            self.restoreState()
    
    def showPage(self):
        self.draw_watermark()
        super(WatermarkCanvas, self).showPage()
    
    def save(self):
        self.draw_watermark()
        super(WatermarkCanvas, self).save()

# Función para generar el reporte (Excel o PDF)
def generar_reporte(nombre_reporte, titulo, registros, keys, formato, headers=None, fondo_imagen=FONDO):
    """
    Genera un reporte en Excel o PDF. Para PDF se utiliza una imagen como marca de agua
    y se crea una tabla cuyos anchos se ajustan proporcionalmente al contenido sin estirar
    las columnas más de lo necesario, dejando un espacio pequeño entre celdas.
    
    :param nombre_reporte: Nombre base del archivo.
    :param titulo: Título del reporte.
    :param registros: Lista de diccionarios con los datos.
    :param keys: Lista con las claves y el orden de las columnas.
    :param formato: 'excel' o 'pdf'.
    :param headers: (Opcional) Encabezados a mostrar; si no se especifica, se usan keys.
    :param fondo_imagen: (Opcional) Ruta a la imagen para la marca de agua.
    :return: Archivo generado (send_file).
    """
    if not registros:
        return jsonify({"error": "No hay datos en el reporte"}), 400
    
    if headers is None:
        headers = keys
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{nombre_reporte}_{fecha_actual}.{formato}"
    
    if formato == "excel":
        df = pd.DataFrame(registros, columns=keys)
        df.columns = headers
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Reporte", index=False)
        output.seek(0)
        return send_file(output,
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         as_attachment=True,
                         download_name=file_name)
    
    elif formato == "pdf":
        output = BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)  # Usamos A3
        elements = []
        styles = getSampleStyleSheet()
        
        # Encabezado del reporte
        elements.append(Paragraph(f"<b>{NOMBRE_EMPRESA}</b>", styles["Title"]))
        elements.append(Paragraph(titulo, styles["Heading2"]))
        elements.append(Paragraph(f"Fecha de Generación: {fecha_actual}", styles["Normal"]))
        elements.append(Spacer(1, 12))
        
        # Preparación de la tabla: primero obtenemos los datos en crudo para medir anchos.
        raw_table_data = [headers] + [[str(registro[key]) for key in keys] for registro in registros]
        # Para A3, asumamos un ancho disponible de 1000 puntos (ajustable según diseño)
        col_widths, gap = ajustar_ancho_columnas_proporcional(raw_table_data,
                                                              fontName="Helvetica",
                                                              fontSize=10,
                                                              padding=5,
                                                              gap=5,
                                                              available_width=540)
        
        # Se crea la tabla usando Paragraphs para permitir el envolvimiento del texto.
        para_style = styles["Normal"]
        wrapped_table_data = []
        wrapped_table_data.append([Paragraph(cell, para_style) for cell in headers])
        for registro in registros:
            wrapped_table_data.append([Paragraph(str(registro[key]), para_style) for key in keys])
        
        table = Table(wrapped_table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (0.851, 0.882, 0.949)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            # Se establece un padding reducido para que no se desperdicie espacio
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(table)
        
        doc.build(elements,canvasmaker=lambda *args, **kwargs: WatermarkCanvas(*args, fondo_imagen=fondo_imagen, **kwargs))
        output.seek(0)
        return send_file(output,mimetype='application/pdf',as_attachment=True,download_name=file_name)
