import customtkinter as ctk
from tkinter import messagebox, END
from Busquda import VentanaBusqueda
from Conexion import (
    obtener_detalle_producto,
    guardarpromocion,
    obtener_promociones,
    cambiar_estado_promocion
)


class FramePromociones(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.codigos_promo = []
        self.mapa_promociones = {}

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        self.izquierda = ctk.CTkFrame(self.contenedor)
        self.izquierda.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.derecha = ctk.CTkFrame(self.contenedor)
        self.derecha.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.nuevos = ctk.CTkLabel(
            self.izquierda,
            text="Agregar una nueva promoción",
            font=("Arial", 18, "bold")
        )
        self.nuevos.pack(pady=5)

        self.nombre = ctk.CTkLabel(
            self.izquierda,
            text="Nombre de la promoción",
            font=("Arial", 12, "bold")
        )
        self.nombre.pack(pady=(5, 2))
        self.nombrebox = ctk.CTkEntry(self.izquierda, width=220)
        self.nombrebox.pack(pady=(0, 5))

        # --- PRIMER PRODUCTO ---
        self.fproducto = ctk.CTkLabel(
            self.izquierda,
            text="Primer producto",
            font=("Arial", 12, "bold")
        )
        self.fproducto.pack(pady=2)
        self.fproductobox = ctk.CTkEntry(self.izquierda, width=220)
        self.fproductobox.pack(pady=2)
        self.fproductobox.configure(state="disabled")

        self.fcantidad = ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.fcantidad.pack(pady=2)
        self.fcantidadbox = ctk.CTkEntry(self.izquierda, width=220)
        self.fcantidadbox.pack(pady=2)
        self.fcantidadbox.configure(state="disabled")

        # --- SEGUNDO PRODUCTO ---
        self.sproducto = ctk.CTkLabel(
            self.izquierda,
            text="Segundo producto",
            font=("Arial", 12, "bold")
        )
        self.sproducto.pack(pady=2)
        self.sproductobox = ctk.CTkEntry(self.izquierda, width=220)
        self.sproductobox.pack(pady=2)
        self.sproductobox.configure(state="disabled")

        self.scantidad = ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.scantidad.pack(pady=2)
        self.scantidadbox = ctk.CTkEntry(self.izquierda, width=220)
        self.scantidadbox.pack(pady=2)
        self.scantidadbox.configure(state="disabled")

        # --- TERCER PRODUCTO ---
        self.tproducto = ctk.CTkLabel(
            self.izquierda,
            text="Tercer producto",
            font=("Arial", 12, "bold")
        )
        self.tproducto.pack(pady=2)
        self.tproductobox = ctk.CTkEntry(self.izquierda, width=220)
        self.tproductobox.pack(pady=2)
        self.tproductobox.configure(state="disabled")

        self.tcantidad = ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.tcantidad.pack(pady=2)
        self.tcantidadbox = ctk.CTkEntry(self.izquierda, width=220)
        self.tcantidadbox.pack(pady=2)
        self.tcantidadbox.configure(state="disabled")

        # --- PRECIO ---
        self.precio = ctk.CTkLabel(
            self.izquierda,
            text="Precio",
            font=("Arial", 12, "bold")
        )
        self.precio.pack(pady=2)
        self.preciobox = ctk.CTkEntry(self.izquierda, width=220)
        self.preciobox.pack(pady=2)

        # --- BOTONES ---
        self.btnbuscar = ctk.CTkButton(
            self.izquierda,
            text="Buscar Producto",
            fg_color="#2535C9",
            hover_color="#170B59",
            text_color="#FFFFFF",
            width=220,
            command=self.buscar
        )
        self.btnbuscar.pack(pady=4)

        self.btnguardar = ctk.CTkButton(
            self.izquierda,
            text="Guardar",
            fg_color="#25C935",
            hover_color="#0B591B",
            text_color="#FFFFFF",
            width=220,
            command=self.guardar
        )
        self.btnguardar.pack(pady=4)

        self.btncancelar = ctk.CTkButton(
            self.izquierda,
            text="Cancelar",
            fg_color="#EF4444",
            hover_color="#6B1818",
            text_color="#FFFFFF",
            width=220,
            command=self.cancelar
        )
        self.btncancelar.pack(pady=4)

        #######################################################
        # CONTROL DE PROMOCIONES (BLOQUE INFERIOR)
        #######################################################
        self.snombre = ctk.CTkLabel(
            self.derecha,
            text="Control de promociones:",
            font=("Arial", 14, "bold")
        )
        self.snombre.pack(side="left", padx=(15, 10), pady=15)

        self.combobox = ctk.CTkComboBox(
            self.derecha,
            values=[],
            width=240,
            state="readonly",
            command=self.al_seleccionar_promo
        )
        self.combobox.pack(side="left", padx=10, pady=15)

        self.switch_activo = ctk.CTkSwitch(
            self.derecha,
            text="Desactivada",
            font=("Arial", 12, "bold"),
            state="disabled",
            command=self.alternar_estado_promo
        )
        self.switch_activo.pack(side="left", padx=15, pady=15)

        self.cargar_promociones()

    def cancelar(self):
        self.codigos_promo.clear()
        self.nombrebox.delete(0, END)
        self.preciobox.delete(0, END)

        cajas = [
            self.fproductobox, self.fcantidadbox,
            self.sproductobox, self.scantidadbox,
            self.tproductobox, self.tcantidadbox
        ]
        for caja in cajas:
            caja.configure(state="normal")
            caja.delete(0, END)
            caja.configure(state="disabled")

        self.btnbuscar.configure(state="normal")

    def guardar(self):
        nombre = self.nombrebox.get().strip()
        precio = self.preciobox.get().strip()

        primer = self.codigos_promo[0] if len(self.codigos_promo) >= 1 else None
        pcantidad = self.fcantidadbox.get().strip()

        segundo = self.codigos_promo[1] if len(self.codigos_promo) >= 2 else None
        scantidad = self.scantidadbox.get().strip() or None

        tercer = self.codigos_promo[2] if len(self.codigos_promo) >= 3 else None
        tcantidad = self.tcantidadbox.get().strip() or None

        if not all([nombre, primer, pcantidad, precio]):
            messagebox.showwarning("Advertencia", "Complete nombre, primer producto, cantidad y precio.")
            return

        if segundo and not scantidad:
            messagebox.showwarning("Advertencia", "Ingrese la cantidad del segundo producto.")
            return

        if tercer and not tcantidad:
            messagebox.showwarning("Advertencia", "Ingrese la cantidad del tercer producto.")
            return

        exito, mensaje = guardarpromocion(
            nombre, primer, pcantidad, segundo, scantidad, tercer, tcantidad, precio
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cargar_promociones()
            self.cancelar()
        else:
            messagebox.showerror("Error", mensaje)

    def buscar(self):
        """Asigna secuencialmente hasta 3 productos y desbloquea su campo de cantidad"""
        if self.tproductobox.get().strip():
            messagebox.showinfo("Límite alcanzado", "Ya seleccionaste los 3 productos permitidos para la promoción.")
            return

        def al_elegir(codigo):
            prod = obtener_detalle_producto(codigo)
            texto_mostrar = f"{codigo} - {prod['nombre']}" if prod else str(codigo)
            self.codigos_promo.append(codigo)

            if not self.fproductobox.get().strip():
                self.fproductobox.configure(state="normal")
                self.fproductobox.delete(0, END)
                self.fproductobox.insert(0, texto_mostrar)
                self.fproductobox.configure(state="disabled")

                self.fcantidadbox.configure(state="normal")
                self.fcantidadbox.focus()

            elif not self.sproductobox.get().strip():
                self.sproductobox.configure(state="normal")
                self.sproductobox.delete(0, END)
                self.sproductobox.insert(0, texto_mostrar)
                self.sproductobox.configure(state="disabled")

                self.scantidadbox.configure(state="normal")
                self.scantidadbox.focus()

            elif not self.tproductobox.get().strip():
                self.tproductobox.configure(state="normal")
                self.tproductobox.delete(0, END)
                self.tproductobox.insert(0, texto_mostrar)
                self.tproductobox.configure(state="disabled")

                self.tcantidadbox.configure(state="normal")
                self.tcantidadbox.focus()
                self.btnbuscar.configure(state="disabled")

        VentanaBusqueda(self, al_seleccionar_callback=al_elegir, modo="ventas")

    def cargar_promociones(self):
        """Consulta MySQL y llena el ComboBox con los nombres de las promociones"""
        promos = obtener_promociones()
        self.mapa_promociones.clear()

        nombres = []
        for p in promos:
            nombre = p["nombre"]
            self.mapa_promociones[nombre] = p
            nombres.append(nombre)

        if nombres:
            self.combobox.configure(values=nombres)
            self.combobox.set("Selecciona una promoción")
        else:
            self.combobox.configure(values=["Sin promociones"])
            self.combobox.set("Sin promociones")

        self.switch_activo.deselect()
        self.switch_activo.configure(text="Desactivada", state="disabled")

    def al_seleccionar_promo(self, nombre_elegido):
        """Sincroniza el switch cuando eliges una promoción en el ComboBox"""
        promo = self.mapa_promociones.get(nombre_elegido)
        if not promo:
            return

        self.switch_activo.configure(state="normal")
        if promo["activo"] == 1:
            self.switch_activo.select()
            self.switch_activo.configure(text="Activa")
        else:
            self.switch_activo.deselect()
            self.switch_activo.configure(text="Desactivada")

    def alternar_estado_promo(self):
        """Guarda en MySQL el cambio entre Activa (1) y Desactivada (0)"""
        nombre_elegido = self.combobox.get()
        promo = self.mapa_promociones.get(nombre_elegido)
        if not promo:
            return

        nuevo_estado = 1 if self.switch_activo.get() == 1 else 0
        exito, mensaje = cambiar_estado_promocion(promo["id"], nuevo_estado)

        if exito:
            promo["activo"] = nuevo_estado
            self.switch_activo.configure(text="Activa" if nuevo_estado == 1 else "Desactivada")
        else:
            messagebox.showerror("Error", mensaje)