import os
from fpdf import FPDF


def generar_factura_pdf(folio, cliente_datos, lista_productos):
    carpeta_facturas = "Facturas"
    os.makedirs(carpeta_facturas, exist_ok=True)
    ruta_pdf = os.path.join(carpeta_facturas, f"Factura_{folio}.pdf")

    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.add_page()

    # --- ENCABEZADO ---
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "FARMACIA - FACTURA DE VENTA", align="C")
    pdf.ln(12)

    # --- DATOS DEL CLIENTE Y FOLIO ---
    nombre = cliente_datos.get("nombre", "publico general")
    rfc = cliente_datos.get("rfc", "XAXX010101000")
    direccion = cliente_datos.get("direccion", "N/A")
    email = cliente_datos.get("email", "N/A")

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(130, 6, f"Cliente: {nombre}")
    pdf.cell(0, 6, f"Folio Factura: #{folio}", align="R")
    pdf.ln()
    pdf.cell(130, 6, f"RFC: {rfc}")
    pdf.cell(0, 6, f"Email: {email}", align="R")
    pdf.ln()
    pdf.cell(0, 6, f"Dirección: {direccion}")
    pdf.ln(10)

    # --- TABLA DE PRODUCTOS ---
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
        pdf.cell(85, 8, str(p["detalles"])[:38], border=1)
        pdf.cell(25, 8, f"${p['precio_unitario']:.2f}", border=1, align="R")
        pdf.cell(25, 8, f"${p['precio_total']:.2f}", border=1, align="R")
        pdf.ln()
        subtotal += p["precio_total"]

    iva = subtotal * 0.16
    total = subtotal + iva

    # --- TOTALES ---
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

    pdf.output(ruta_pdf)
    os.startfile(ruta_pdf)