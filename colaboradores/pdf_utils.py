"""
Generación del PDF de horarios con reportlab.

Se usa reportlab porque no requiere dependencias externas del sistema
(a diferencia de weasyprint, que necesita librerías de sistema para
renderizar HTML/CSS). El diseño se arma directamente con tablas.
"""

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ROJO_CINEPOLIS = colors.HexColor("#8A0E2E")
GRIS_OSCURO = colors.HexColor("#2B2B2B")
GRIS_CLARO = colors.HexColor("#F4F4F4")


def generar_pdf_horarios(area, filas, dias):
    """
    area: nombre del área o "Todas las áreas"
    filas: lista de tuplas (colaborador_dict, semana_dict) donde
           semana_dict = { "Lunes": {"area":..,"entrada":..,"salida":..}, ... }
    dias: lista ordenada de días de la semana
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.3 * cm,
        bottomMargin=1.3 * cm,
    )

    estilos = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        "TituloCinepolis", parent=estilos["Title"], textColor=ROJO_CINEPOLIS, fontSize=20,
    )
    estilo_sub = ParagraphStyle(
        "SubCinepolis", parent=estilos["Normal"], textColor=GRIS_OSCURO, fontSize=11,
    )

    elementos = []
    elementos.append(Paragraph("Cinépolis · Unidad (proyecto de estadía)", estilo_sub))
    elementos.append(Paragraph("Horario de Colaboradores", estilo_titulo))
    elementos.append(Paragraph(f"Área: {area}", estilo_sub))
    elementos.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilo_sub))
    elementos.append(Spacer(1, 0.5 * cm))

    encabezado = ["Colaborador"] + dias
    filas_tabla = [encabezado]

    for colaborador, semana in filas:
        fila = [colaborador["nombre"]]
        for dia in dias:
            turno = semana.get(dia, {})
            if turno.get("area"):
                fila.append(f"{turno['entrada']}-{turno['salida']}\n{turno['area']}")
            else:
                fila.append("Descanso")
        filas_tabla.append(fila)

    tabla = Table(filas_tabla, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ROJO_CINEPOLIS),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GRIS_CLARO]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elementos.append(tabla)
    doc.build(elementos)

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
