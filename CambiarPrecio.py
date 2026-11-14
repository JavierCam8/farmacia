import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, END
from Conexion import validar

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class confirmacion(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Verificacion")
        self.geometry("150x200")
        self.resizable(False, False)

        self.lusuario=ctk.CTkLabel(
            self,
            text="Contraseña nivel admin",
            font=("Arial", 12, "bold")
        )
        self.lusuario.place(pady=5)
        self.lusuariobox=ctk.CTkEntry(self, width=100)
        self.lusuario.pack(pady=3)

        self.lpassword=ctk.CTkLabel(
            self,
            text="Contraseña nivel admin",
            font=("Arial", 12, "bold")
        )
        self.lpassword.place(pady=5)
        self.passbox=ctk.CTkEntry(self, width=100)
        self.passbox.pack(pady=3)

        self.btn_verificar=ctk.CTkButton(
            self,
            text="Verificar",
            fg_color="#33A018",
            hover_color="#136C13",
            text_color="#FFFFFF",
            width=100,
            command= self.verificar
        )
        self.btn_verificar.pack(pady=5)

        self.btn_cancelar=ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#DB2020",
            hover_color="#8A1616",
            text_color="#FFFFFF",
            width=100,
            command= self.cancelar
        )
        self.btn_cancelar.pack(pady=5)

    def verificar(self):
        usuario = self.lusuariobox.get().strip()
        password = self.passbox.get().strip()

        if not usuario or password:
            messagebox.showinfo("Falta", "Falta llenar campos")
            return
        datos=validar(usuario, password)

        if datos:
            self.destroy
            ####
        else:
            messagebox.showwarning("Error", "Contraseña o usuario incorrectas")
            return
        
    def cancelar(self):
        self.destroy

class Cambio_precio(ctk.CTkToplevel):
    def __init__(self):
        super. __init__()
        self.title("Cambiar precio")
        self.geometry("400x500")
        self.resizable(False, False)

        self.lnombre=ctk.CTkLabel(
            self,
            text="Nombre del producto",
            font=("Arial", 12, "bold")
        )
        self.lnombre.pack(side="left", pady= 5, padx=10)
        self.lnombrebox=ctk.CTkEntry(self, width=200)
        self.lnombrebox.pack(side="left", pady=5, padx=10)

        self.lprecio=ctk.CTkLabel(
            self,
            text="Precio del producto",
            font=("Arial", 12, "bold")
        )
        self.lprecio.pack(side="left", pady=10, padx=10)
        self.lpreciobox=ctk.CTkEntry(self, width=200)
        self.lpreciobox.pack(side="left", pady=10, padx=10)

        self.lnuevoprecio=ctk.CTkLabel(
            self,
            text="Nuevo Precio",
            font=("Arial", 12, "bold")
        )
        self.lnuevoprecio.pack(side="left", pady=15, padx=10)
        self.lnuevopreciobox=ctk.CTkEntry(self, width=200)
        self.lnuevoprecio.pack(side="left", pady=15, padx=10)

        self. btncambiar=ctk.CTkButton(
            self,
            text="Cambiar",
            fg_color="#2E9919",
            hover="#287E17",
            text_color="#FFFFFF",
            width=100,
            command= self.cambiar
        )
        self.btncambiar.pack(side="left", pady=20, padx=10)

        self. btncancelar=ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#D30B0B",
            hover="#7E1717",
            text_color="#FFFFFF",
            width=100,
            command= self.cancelar
        )
        self.btncancelar.pack(side="left", pady=20, padx=10)

    def cambiar(self):
        pass
    def cancelar(self):
        self.destroy
        