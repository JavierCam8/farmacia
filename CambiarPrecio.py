import customtkinter as ctk
from tkinter import messagebox
from Conexion import validar


class confirmacion(ctk.CTkToplevel):
    def __init__(self, parent, al_autorizar_callback=None):
        super().__init__(parent)
        self.title("Verificación")
        self.geometry("300x260")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.al_autorizar_callback = al_autorizar_callback

        self.lusuario = ctk.CTkLabel(
            self,
            text="Usuario nivel admin:",
            font=("Arial", 12, "bold")
        )
        self.lusuario.pack(pady=(20, 5))
        self.lusuariobox = ctk.CTkEntry(self, width=200)
        self.lusuariobox.pack(pady=3)

        self.lpassword = ctk.CTkLabel(
            self,
            text="Contraseña nivel admin:",
            font=("Arial", 12, "bold")
        )
        self.lpassword.pack(pady=(10, 5))
        self.passbox = ctk.CTkEntry(self, width=200, show="*")
        self.passbox.pack(pady=3)

        frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_btns.pack(pady=20)

        self.btn_verificar = ctk.CTkButton(
            frame_btns,
            text="Verificar",
            fg_color="#33A018",
            hover_color="#136C13",
            text_color="#FFFFFF",
            width=100,
            command=self.verificar
        )
        self.btn_verificar.pack(side="left", padx=5)

        self.btn_cancelar = ctk.CTkButton(
            frame_btns,
            text="Cancelar",
            fg_color="#DB2020",
            hover_color="#8A1616",
            text_color="#FFFFFF",
            width=100,
            command=self.cancelar
        )
        self.btn_cancelar.pack(side="left", padx=5)

        self.after(100, lambda: self.lusuariobox.focus())

    def verificar(self):
        usuario = self.lusuariobox.get().strip()
        password = self.passbox.get().strip()

        if not usuario or not password:
            messagebox.showinfo("Falta", "Falta llenar campos")
            return

        datos = validar(usuario, password)

        if datos:
            self.destroy()
            if self.al_autorizar_callback:
                self.al_autorizar_callback()
        else:
            messagebox.showwarning("Error", "Contraseña o usuario incorrectos")

    def cancelar(self):
        self.destroy()


class Cambio_precio(ctk.CTkToplevel):
    def __init__(self, parent, nombre_producto, precio_actual, al_cambiar_callback=None):
        super().__init__(parent)
        self.title("Cambiar precio")
        self.geometry("360x340")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.al_cambiar_callback = al_cambiar_callback

        self.lnombre = ctk.CTkLabel(
            self,
            text="Producto:",
            font=("Arial", 12, "bold")
        )
        self.lnombre.pack(pady=(20, 3))
        self.lnombrebox = ctk.CTkEntry(self, width=260)
        self.lnombrebox.insert(0, nombre_producto)
        self.lnombrebox.configure(state="disabled")
        self.lnombrebox.pack(pady=3)

        self.lprecio = ctk.CTkLabel(
            self,
            text="Precio actual:",
            font=("Arial", 12, "bold")
        )
        self.lprecio.pack(pady=(12, 3))
        self.lpreciobox = ctk.CTkEntry(self, width=260)
        self.lpreciobox.insert(0, f"{float(precio_actual):.2f}")
        self.lpreciobox.configure(state="disabled")
        self.lpreciobox.pack(pady=3)

        self.lnuevoprecio = ctk.CTkLabel(
            self,
            text="Nuevo Precio:",
            font=("Arial", 12, "bold")
        )
        self.lnuevoprecio.pack(pady=(12, 3))
        self.lnuevopreciobox = ctk.CTkEntry(self, width=260, placeholder_text="0.00")
        self.lnuevopreciobox.pack(pady=3)

        frame_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_btns.pack(pady=25)

        self.btncambiar = ctk.CTkButton(
            frame_btns,
            text="Cambiar",
            fg_color="#2E9919",
            hover_color="#287E17",
            text_color="#FFFFFF",
            width=110,
            command=self.cambiar
        )
        self.btncambiar.pack(side="left", padx=8)

        self.btncancelar = ctk.CTkButton(
            frame_btns,
            text="Cancelar",
            fg_color="#D30B0B",
            hover_color="#7E1717",
            text_color="#FFFFFF",
            width=110,
            command=self.cancelar
        )
        self.btncancelar.pack(side="left", padx=8)

        self.after(100, lambda: self.lnuevopreciobox.focus())

    def cambiar(self):
        valor = self.lnuevopreciobox.get().strip()
        try:
            nuevo_precio = float(valor)
            if nuevo_precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto numérico válido.")
            return

        if self.al_cambiar_callback:
            self.al_cambiar_callback(nuevo_precio)
        self.destroy()

    def cancelar(self):
        self.destroy()