import customtkinter as ctk
from tkinter import messagebox, END

class Notanueva(ctk.CTkToplevel):
    def __init__(self, parent, al_confirmar_callback=None):
        super().__init__()
        self.title("Nueva nota")
        self.geometry("320x180")
        self.resizable(False, False)

        self.al_confirmar_callback=al_confirmar_callback

        self.litulo=ctk.CTkLabel(
            self,
            text="Desea agregar una nueva nota:",
            font=("Arial", 14, "bold")
        )
        self.litulo.pack(pady=5)

        self.btnacept=ctk.CTkButton(
            self,
            text="Agregar",
            fg_color="#21B719",
            hover_color="#1C7E17",
            text_color="#FFFFFF",
            width=180,
            command= self.agregar
        )
        self.btnacept.pack(pady=10)

        self.btncancelar=ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#B71919",
            hover_color="#931212",
            text_color="#FFFFFF",
            width=180,
            command= self.cancelar
        )
        self.btncancelar.pack(pady=4)

    def cancelar(self):
        self.destroy()
        return
    def agregar(self, lista_productos):
        self.destroy()
        if self.al_confirmar_callback:
            self.al_confirmar_callback()
    
