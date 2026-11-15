import os

def generar_ticket_txt(folio, cliente, lista_productos):
    carpeta = "Tickets"
    os.makedirs(carpeta, exist_ok=True)
    ruta_archivo = os.path.join(carpeta, f"Ticket_{folio}.txt")

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("========================================\n")
        archivo.write("          FARMACIA - TICKET             \n")
        archivo.write("========================================\n")
        archivo.write(f"Folio:   #{folio}\n")
        archivo.write(f"Cliente: {cliente}\n")
        archivo.write("----------------------------------------\n")
        archivo.write("CANT  DESCRIPCIÓN              IMPORTE\n")
        archivo.write("----------------------------------------\n")

        subtotal = 0.0
        for p in lista_productos:
            cant = str(p["cantidad"]).ljust(5)
            desc = str(p["detalles"])[:22].ljust(23)
            importe = f"${p['precio_total']:.2f}".rjust(10)
            archivo.write(f"{cant} {desc} {importe}\n")
            subtotal += p["precio_total"]

        iva = subtotal * 0.16
        total = subtotal + iva

        archivo.write("----------------------------------------\n")
        archivo.write(f"Subtotal: ${subtotal:.2f}\n")
        archivo.write(f"IVA 16%:  ${iva:.2f}\n")
        archivo.write(f"TOTAL:    ${total:.2f}\n")
        archivo.write("========================================\n")
        archivo.write("        ¡Gracias por su compra!         \n")

    os.startfile(ruta_archivo)