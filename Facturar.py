import os
from fpdf import FPDF

def generar_nota_pdf(folio, cliente, lista_productos):
    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "FARMACIA - NOTA DE VENTA", align="C")
    pdf.ln(12)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(100, 7, f"Cliente: {cliente}")
    pdf.cell(0, 7, f"Folio: #{folio}", align="R")
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(220, 220, 220) 
    pdf.cell(35, 8, "Código", border=1, fill=True)
    pdf.cell(20, 8, "Cant.", border=1, align="C", fill=True)
    pdf.cell(85, 8, "Descripción", border=1, fill=True)
    pdf.cell(25, 8, "P. Unit.", border=1, align="R", fill=True)
    pdf.cell(25, 8, "Total", border=1, align="R", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)
    subtotal = 0.0

    for p in lista_productos:
        pdf.cell(35, 8, str(p["codigo"]), border=1)
        pdf.cell(20, 8, str(p["cantidad"]), border=1, align="C")
        # [:38] recorta textos muy largos para que no se salgan de la celda
        pdf.cell(85, 8, str(p["detalles"])[:38], border=1)
        pdf.cell(25, 8, f"${p['precio_unitario']:.2f}", border=1, align="R")
        pdf.cell(25, 8, f"${p['precio_total']:.2f}", border=1, align="R")
        pdf.ln()
        subtotal += p["precio_total"]

    iva = subtotal * 0.16
    total = subtotal + iva

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(165, 7, "Subtotal:", align="R")
    pdf.cell(25, 7, f"${subtotal:.2f}", align="R")
    pdf.ln()

    pdf.cell(165, 7, "IVA (16%):", align="R")
    pdf.cell(25, 7, f"${iva:.2f}", align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(165, 8, "TOTAL:", align="R")
    pdf.cell(25, 8, f"${total:.2f}", align="R")
    pdf.ln()

    carpeta_destino= "Facturas"
    nombre_archivo = f"Nota_{folio}.pdf"
    os.makedirs(carpeta_destino, exist_ok=True)

    rutas_de_archivo=os.path.join(carpeta_destino,nombre_archivo)
    
    pdf.output(rutas_de_archivo)
    os.startfile(rutas_de_archivo)

