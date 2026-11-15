import customtkinter as ctk
import os


class Notanueva(ctk.CTkToplevel):
    def __init__(self, parent, al_confirmar_callback=None):
        super().__init__(parent)
        self.title("Nueva nota")
        self.geometry("320x180")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.al_confirmar_callback = al_confirmar_callback

        self.ltitulo = ctk.CTkLabel(
            self,
            text="¿Desea guardar la nota actual\ne iniciar una nueva?",
            font=("Arial", 14, "bold")
        )
        self.ltitulo.pack(pady=(15, 10))

        self.btnacept = ctk.CTkButton(
            self,
            text="Agregar",
            fg_color="#21B719",
            hover_color="#1C7E17",
            text_color="#FFFFFF",
            width=180,
            command=self.agregar
        )
        self.btnacept.pack(pady=6)

        self.btncancelar = ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#B71919",
            hover_color="#931212",
            text_color="#FFFFFF",
            width=180,
            command=self.cancelar
        )
        self.btncancelar.pack(pady=4)

    def cancelar(self):
        self.destroy()

    def agregar(self):
        self.destroy()
        if self.al_confirmar_callback:
            self.al_confirmar_callback()


def guardar_nota_txt(folio, cliente, lista_productos):
    carpeta = "Notas"
    os.makedirs(carpeta, exist_ok=True)
    ruta_archivo = os.path.join(carpeta, f"Nota_{folio}.txt")

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("========================================\n")
        archivo.write(f"Folio:   #{folio}\n")
        archivo.write(f"Cliente: {cliente}\n")
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