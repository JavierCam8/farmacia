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


class Buscarnota(ctk.CTkToplevel):
    def __init__(self, parent, lista_folios, seleccionarcallback=None):
        super().__init__(parent)
        self.title("Buscar Notas")
        self.geometry("300x180")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.seleccionarcallback=seleccionarcallback

        self.lbuscar=ctk.CTkLabel(
            self,
            text="Seleccione el numero de folio:"
            font=("Arial", 14, "bold")
        )
        self.lbuscar.pack(pady=(15, 8))

        self.combofolio=ctk.CTkComboBox(
            self,
            values=lista_folios,
            width=200,
            state="readonly"
        )
        self.combofolio.pack(pady=5)
        if lista_folios:
            self.combofolio.set(lista_folios[0])

        self.btncargar=ctk.CTkButton(
            self,
            text="Cargar Notas",
            fg_color="#21B719",
            hover_color="#1C7E17",
            width=200,
            command=self.cargar
        )
        self.btncargar.pack(pady=(15, 5))
    def cargar(self):
        folio_elegido=self.combofolio.get()
        self.destroy()
        if self.seleccionarcallback and folio_elegido:
            self.seleccionarcallback(folio_elegido)

class Cancelarnota(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cancelar nota")
        self.geometry("400x500")
        self.resizable(False, False)

        self.buscarnota=ctk.CTkLabel(
            self,
            text="Seleccione la nota para cancelar",
            font=("Arial", 12, "bold")
        )
        self.buscarnota.pack(pady=5)
        self.combonotas=ctk.CTkComboBox(
            self,

        )


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