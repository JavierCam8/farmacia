import customtkinter as ctk
from tkinter import messagebox, END
from Conexion import (
    guardarcliente,
    obtener_clientes,
    buscarcliente_nombre,
    actualizarcliente,
)


class FrameClientes(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.cliente_actual_id = None

        self.label_titulo = ctk.CTkLabel(
            self,
            text="Información del cliente",
            font=("Arial", 18, "bold")
        )
        self.label_titulo.pack(pady=(15, 10))

        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal.pack(fill="both", expand=True, padx=15, pady=10)

        # ====================================================
        # COLUMNA IZQUIERDA: FORMULARIO DE CLIENTE
        # ====================================================
        self.frame_informacion = ctk.CTkFrame(self.contenedor_principal)
        self.frame_informacion.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.lbframe2 = ctk.CTkLabel(
            self.frame_informacion,
            text="Revisar o registrar un Cliente",
            font=("Arial", 18, "bold")
        )
        self.lbframe2.pack(anchor="w", padx=15, pady=(15, 10))

        self.inelejir = ctk.CTkLabel(
            self.frame_informacion,
            text="Seleccione nombre:",
            font=("Arial", 12, "bold")
        )
        self.inelejir.pack(anchor="nw", pady=(0, 3), padx=15)
        self.innombre = ctk.CTkComboBox(
            self.frame_informacion,
            values=[""],
            width=300,
            command=self.cargar_datos_cliente
        )
        self.innombre.pack(anchor="nw", pady=(0, 5), padx=15)

        self.inombre = ctk.CTkLabel(self.frame_informacion, text="Nombre:", font=("Arial", 12, "bold"))
        self.inombre.pack(anchor="nw", pady=2, padx=15)
        self.innombrebox = ctk.CTkEntry(self.frame_informacion, width=300)
        self.innombrebox.pack(anchor="nw", pady=2, padx=15)

        self.inuser = ctk.CTkLabel(self.frame_informacion, text="Código del Cliente:", font=("Arial", 12, "bold"))
        self.inuser.pack(anchor="nw", pady=2, padx=15)
        self.inuserbox = ctk.CTkEntry(self.frame_informacion, width=300)
        self.inuserbox.pack(anchor="nw", pady=2, padx=15)

        self.intelefono = ctk.CTkLabel(self.frame_informacion, text="Teléfono:", font=("Arial", 12, "bold"))
        self.intelefono.pack(anchor="nw", pady=2, padx=15)
        self.intelefonobox = ctk.CTkEntry(self.frame_informacion, width=300)
        self.intelefonobox.pack(anchor="nw", pady=2, padx=15)

        self.inrfc = ctk.CTkLabel(self.frame_informacion, text="RFC:", font=("Arial", 12, "bold"))
        self.inrfc.pack(anchor="nw", pady=2, padx=15)
        self.inrfcbox = ctk.CTkEntry(self.frame_informacion, width=300)
        self.inrfcbox.pack(anchor="nw", pady=2, padx=15)

        self.inestado = ctk.CTkLabel(self.frame_informacion, text="Estado:", font=("Arial", 12, "bold"))
        self.inestado.pack(anchor="nw", pady=2, padx=15)
        self.inestadobox = ctk.CTkEntry(self.frame_informacion, width=300)
        self.inestadobox.pack(anchor="nw", pady=2, padx=15)

        self.indireccion = ctk.CTkLabel(self.frame_informacion, text="Dirección:", font=("Arial", 12, "bold"))
        self.indireccion.pack(anchor="nw", pady=2, padx=15)
        self.indireccionbox = ctk.CTkEntry(self.frame_informacion, width=300)
        self.indireccionbox.pack(anchor="nw", pady=2, padx=15)

        self.inemail = ctk.CTkLabel(self.frame_informacion, text="Email:", font=("Arial", 12, "bold"))
        self.inemail.pack(anchor="nw", pady=2, padx=15)
        self.inemailbox = ctk.CTkEntry(self.frame_informacion, width=300)
        self.inemailbox.pack(anchor="nw", pady=(2, 8), padx=15)

        self.btnguardarcambio = ctk.CTkButton(
            self.frame_informacion,
            text="Guardar Nuevo",
            fg_color="#0DAA12",
            hover_color="#17760B",
            text_color="#FFFFFF",
            width=300,
            command=self.registrar
        )
        self.btnguardarcambio.pack(anchor="nw", pady=2, padx=15)

        self.btchange = ctk.CTkButton(
            self.frame_informacion,
            text="Cambiar información",
            fg_color="#2456D4",
            hover_color="#0F0DAA",
            text_color="#FEFEFE",
            width=300,
            state="disabled",
            command=self.cambiar
        )
        self.btchange.pack(anchor="nw", pady=2, padx=15)

        self.btdespedir = ctk.CTkButton(
            self.frame_informacion,
            text="Cancelar",
            fg_color="#CC2525",
            hover_color="#5B0A0A",
            text_color="#ECE9E9",
            width=300,
            command=self.cancelar
        )
        self.btdespedir.pack(anchor="nw", pady=2, padx=15)

        # ====================================================
        # COLUMNA DERECHA: PUNTOS Y DINERO GASTADO
        # ====================================================
        self.frame_agregar = ctk.CTkFrame(self.contenedor_principal, width=320)
        self.frame_agregar.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.lbagregar = ctk.CTkLabel(
            self.frame_agregar,
            text="Programa de Lealtad",
            font=("Arial", 18, "bold")
        )
        self.lbagregar.pack(pady=(15, 10), anchor="w", padx=15)

        self.puntos = ctk.CTkLabel(
            self.frame_agregar,
            text="Puntos acumulados del cliente:",
            font=("Arial", 12, "bold")
        )
        self.puntos.pack(pady=(10, 4), anchor="w", padx=15)
        self.puntosbox = ctk.CTkEntry(self.frame_agregar, width=260)
        self.puntosbox.pack(pady=(0, 6), anchor="w", padx=15)
        self.puntosbox.configure(state="disabled")

        self.lbl_estado_canje = ctk.CTkLabel(
            self.frame_agregar,
            text="Seleccione un cliente para consultar sus puntos.",
            font=("Arial", 12, "bold"),
            text_color="#A1A1AA"
        )
        self.lbl_estado_canje.pack(pady=(0, 15), anchor="w", padx=15)

        self.historial = ctk.CTkLabel(
            self.frame_agregar,
            text="Dinero gastado acumulado:",
            font=("Arial", 12, "bold")
        )
        self.historial.pack(pady=(10, 4), anchor="w", padx=15)
        self.gastobox = ctk.CTkEntry(self.frame_agregar, width=260)
        self.gastobox.pack(pady=(0, 15), anchor="w", padx=15)
        self.gastobox.configure(state="disabled")

        self.card_reglas = ctk.CTkFrame(self.frame_agregar, fg_color="#2B2B2B", corner_radius=8)
        self.card_reglas.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(
            self.card_reglas,
            text="Reglas de Puntos:\n• Compras mayores a $200.00 acumulan +5 puntos.\n• Al juntar 50 puntos, la siguiente compra menor a $200.00 es gratis.",
            font=("Arial", 12),
            justify="left",
            text_color="#D4D4D8"
        ).pack(anchor="w", padx=12, pady=10)

        self.cargar_lista_clientes()

    def refrescar_listas(self):
        """Actualiza los datos al volver a abrir la pestaña Clientes"""
        seleccion = self.innombre.get().strip()
        self.cargar_lista_clientes()
        if seleccion:
            self.innombre.set(seleccion)
            self.cargar_datos_cliente(seleccion)

    def cargar_lista_clientes(self):
        clientes = obtener_clientes()
        nombres = [c["nombre"] for c in clientes]
        self.innombre.configure(values=nombres if nombres else [""])
        self.innombre.set("")

    def cargar_datos_cliente(self, _seleccion=None):
        nombre = self.innombre.get().strip()
        if not nombre:
            return

        datos = buscarcliente_nombre(nombre)
        if not datos:
            messagebox.showwarning("Sin resultados", "No se encontró el cliente.")
            return

        self.cliente_actual_id = datos["id"]
        self.btchange.configure(state="normal")
        self.btnguardarcambio.configure(state="disabled")

        self.innombrebox.delete(0, END)
        self.innombrebox.insert(0, datos.get("nombre") or "")

        self.inuserbox.delete(0, END)
        self.inuserbox.insert(0, datos.get("codigo") or "")

        self.intelefonobox.delete(0, END)
        self.intelefonobox.insert(0, datos.get("telefono") or "")

        self.inrfcbox.delete(0, END)
        self.inrfcbox.insert(0, datos.get("rfc") or "")

        self.inestadobox.delete(0, END)
        self.inestadobox.insert(0, datos.get("estado") or "")

        self.indireccionbox.delete(0, END)
        self.indireccionbox.insert(0, datos.get("direccion") or "")

        self.inemailbox.delete(0, END)
        self.inemailbox.insert(0, datos.get("email") or "")

        pts = int(datos.get("puntos") or 0)
        gasto = float(datos.get("dinerogastado") or 0)

        self.puntosbox.configure(state="normal")
        self.puntosbox.delete(0, END)
        self.puntosbox.insert(0, f"{pts} puntos")
        self.puntosbox.configure(state="disabled")

        self.gastobox.configure(state="normal")
        self.gastobox.delete(0, END)
        self.gastobox.insert(0, f"${gasto:,.2f}")
        self.gastobox.configure(state="disabled")

        if int(datos["id"]) == 1:
            self.lbl_estado_canje.configure(text="Cliente genérico (no acumula puntos).", text_color="#A1A1AA")
        elif pts >= 50:
            self.lbl_estado_canje.configure(text="¡Disponible para compra gratis menor a $200.00!", text_color="#4ADE80")
        else:
            faltan = 50 - pts
            self.lbl_estado_canje.configure(text=f"Faltan {faltan} puntos para canjear compra gratis.", text_color="#60A5FA")

    def registrar(self):
        codigo = self.inuserbox.get().strip()
        nombre = self.innombrebox.get().strip()
        telefono = self.intelefonobox.get().strip()
        rfc = self.inrfcbox.get().strip()
        direccion = self.indireccionbox.get().strip()
        estado = self.inestadobox.get().strip()
        email = self.inemailbox.get().strip()

        if not all([codigo, nombre, telefono, rfc, direccion, estado, email]):
            messagebox.showerror("Error", "Datos incompletos.")
            return

        exito, mensaje = guardarcliente(nombre, telefono, rfc, email, direccion, estado, codigo)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
            self.cargar_lista_clientes()
        else:
            messagebox.showerror("Error", mensaje)

    def cambiar(self):
        if not self.cliente_actual_id:
            messagebox.showerror("Error", "Seleccione un cliente primero.")
            return

        codigo = self.inuserbox.get().strip()
        nombre = self.innombrebox.get().strip()
        telefono = self.intelefonobox.get().strip()
        rfc = self.inrfcbox.get().strip()
        direccion = self.indireccionbox.get().strip()
        estado = self.inestadobox.get().strip()
        email = self.inemailbox.get().strip()

        exito, mensaje = actualizarcliente(
            self.cliente_actual_id, nombre, telefono, rfc, email, direccion, estado, codigo
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
            self.cargar_lista_clientes()
        else:
            messagebox.showerror("Error", mensaje)

    def cancelar(self):
        self.cliente_actual_id = None
        self.innombre.set("")
        self.inuserbox.delete(0, END)
        self.innombrebox.delete(0, END)
        self.intelefonobox.delete(0, END)
        self.inrfcbox.delete(0, END)
        self.inestadobox.delete(0, END)
        self.indireccionbox.delete(0, END)
        self.inemailbox.delete(0, END)

        self.puntosbox.configure(state="normal")
        self.puntosbox.delete(0, END)
        self.puntosbox.configure(state="disabled")

        self.gastobox.configure(state="normal")
        self.gastobox.delete(0, END)
        self.gastobox.configure(state="disabled")

        self.lbl_estado_canje.configure(
            text="Seleccione un cliente para consultar sus puntos.",
            text_color="#A1A1AA"
        )
        self.btchange.configure(state="disabled")
        self.btnguardarcambio.configure(state="normal")