import customtkinter as ctk
from tkinter import messagebox, END

class promociones(ctk.CTkFrame):
    def __init__(self, parent):
        super(). __init__(parent)

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        self.izquierda = ctk.CTkFrame(self.contenedor)
        self.izquierda.pack(side="top", fill="both", expand=True, pady=(0, 10))

        self.derecha = ctk.CTkFrame(self.contenedor, height=90)
        self.derecha.pack(side="top", fill="x", pady=(10, 0))

        self.nuevos=ctk.CTkLabel(
            self.izquierda,
            text="Agregar una nueva promocion",
            font=("Arial", 18, "bold")
        )
        self.nuevos.pack(pady=5)

        self.condicion=ctk.CTkLabel(
            self.izquierda,
            text="Introducior codigo o codigo de barras",
            font=("Arial", 18, "bold")
        )
        self.condicion.pack(pady=5)

        self.fproducto=ctk.CTkLabel(
            self.izquierda,
            text="Primer producto",
            font=("Arial", 12, "bold")
        )
        self.fproducto.pack(pady=5)
        self.fproductobox=ctk.CTkEntry(self.izquierda, width=200)
        self.fproductobox.pack(pady=5)
        self.fcantidad=ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.fcantidad.pack(pady=5)
        self.fcantidadbox=ctk.CTkEntry(self.izquierda, width=200)
        self.fcantidadbox.pack(pady=5)

        self.sproducto=ctk.CTkLabel(
            self.izquierda,
            text="Segundo producto",
            font=("Arial", 12, "bold")
        )
        self.sproducto.pack(pady=5)
        self.sproductobox=ctk.CTkEntry(self.izquierda, width=200)
        self.sproductobox.pack(pady=5)
        self.sproductobox.configure(state="disabled")
        self.scantidad=ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.scantidad.pack(pady=5)
        self.scantidadbox=ctk.CTkEntry(self.izquierda, width=200)
        self.scantidadbox.pack(pady=5)
        self.scantidadbox.configure(state="disabled")


        self.tproducto=ctk.CTkLabel(
            self.izquierda,
            text="Tercer producto",
            font=("Arial", 12, "bold")
        )
        self.tproducto.pack(pady=5)
        self.tproductobox=ctk.CTkEntry(self.izquierda, width=200)
        self.tproductobox.pack(pady=5)
        self.tproductobox.configure(state="disabled")
        self.tcantidad=ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.tcantidad.pack(pady=5)
        self.tcantidadbox=ctk.CTkEntry(self.izquierda, width=200)
        self.tcantidadbox.pack(pady=5)
        self.tcantidadbox.configure(state="disabled")

        self.btnguardar=ctk.CTkButton(
            self.izquierda,
            text="Guardar",
            
        )