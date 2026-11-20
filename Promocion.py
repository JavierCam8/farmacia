import customtkinter as ctk
from tkinter import messagebox, END
from Busquda import VentanaBusqueda
from Conexion import (
    obtener_detalle_producto,
    guardarpromocion,
    obtener_promociones_completas,
    cambiar_estado_promocion,
    eliminarpromocion,
)


class FramePromociones(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.codigos_promo = []
        self.mapa_promociones = {}

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        # ====================================================
        # COLUMNA IZQUIERDA: FORMULARIO DE NUEVA PROMOCIÓN
        # ====================================================
        self.izquierda = ctk.CTkFrame(self.contenedor)
        self.izquierda.pack(side="left", fill="both", expand=True, padx=(0, 10))

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

        # ====================================================
        # COLUMNA DERECHA: PANEL DE GESTIÓN Y VISTA PREVIA
        # ====================================================
        self.derecha = ctk.CTkFrame(self.contenedor)
        self.derecha.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.titulo_derecha = ctk.CTkLabel(
            self.derecha,
            text="Administración de Promociones",
            font=("Arial", 18, "bold")
        )
        self.titulo_derecha.pack(pady=(12, 8))

        # 1. TARJETAS DE CONTADORES SUPERIORES (3 columnas)
        self.frame_kpis = ctk.CTkFrame(self.derecha, fg_color="transparent")
        self.frame_kpis.pack(fill="x", padx=15, pady=(0, 10))
        self.frame_kpis.grid_columnconfigure((0, 1, 2), weight=1)

        self.lbl_total_promos = self.crear_kpi(self.frame_kpis, 0, "Total Registradas", "0", "#3B82F6")
        self.lbl_activas_promos = self.crear_kpi(self.frame_kpis, 1, "Promociones Activas", "0", "#10B981")
        self.lbl_inactivas_promos = self.crear_kpi(self.frame_kpis, 2, "Desactivadas", "0", "#EF4444")

        # 2. BARRA DE CONTROL DE PROMOCIONES (Selector + Switch + Eliminar)
        self.card_control = ctk.CTkFrame(self.derecha, fg_color="#2B2B2B", corner_radius=10)
        self.card_control.pack(fill="x", padx=15, pady=(0, 10))

        self.snombre = ctk.CTkLabel(
            self.card_control,
            text="Control de promociones:",
            font=("Arial", 13, "bold")
        )
        self.snombre.pack(side="left", padx=(12, 8), pady=12)

        self.combobox = ctk.CTkComboBox(
            self.card_control,
            values=["Sin promociones"],
            width=210,
            state="readonly",
            command=self.al_seleccionar_promo
        )
        self.combobox.pack(side="left", padx=6, pady=12)

        self.switch_activo = ctk.CTkSwitch(
            self.card_control,
            text="Desactivada",
            font=("Arial", 12, "bold"),
            state="disabled",
            command=self.alternar_estado_promo
        )
        self.switch_activo.pack(side="left", padx=10, pady=12)

        self.btn_eliminar = ctk.CTkButton(
            self.card_control,
            text="Eliminar",
            width=90,
            height=30,
            fg_color="#DC2626",
            hover_color="#991B1B",
            font=("Arial", 12, "bold"),
            state="disabled",
            command=self.eliminar_promo_actual
        )
        self.btn_eliminar.pack(side="right", padx=12, pady=12)

        # 3. TARJETA DE VISTA PREVIA Y CÁLCULO DE AHORRO
        self.card_detalle = ctk.CTkFrame(self.derecha, fg_color="#2B2B2B", corner_radius=10)
        self.card_detalle.pack(fill="x", padx=15, pady=(0, 10))

        self.lbl_detalle_titulo = ctk.CTkLabel(
            self.card_detalle,
            text="Detalle y Ahorro del Paquete",
            font=("Arial", 13, "bold"),
            text_color="#60A5FA"
        )
        self.lbl_detalle_titulo.pack(anchor="w", padx=12, pady=(8, 4))

        self.lbl_detalle_productos = ctk.CTkLabel(
            self.card_detalle,
            text="Seleccione una promoción de la lista o del menú superior para ver su contenido.",
            font=("Arial", 12),
            text_color="#D4D4D8",
            justify="left"
        )
        self.lbl_detalle_productos.pack(anchor="w", padx=12, pady=(0, 6))

        self.frame_precios_detalle = ctk.CTkFrame(self.card_detalle, fg_color="#232323", corner_radius=6)
        self.frame_precios_detalle.pack(fill="x", padx=12, pady=(0, 10))

        self.lbl_precio_regular = ctk.CTkLabel(
            self.frame_precios_detalle,
            text="Precio regular: $0.00",
            font=("Arial", 12, "bold"),
            text_color="#A1A1AA"
        )
        self.lbl_precio_regular.pack(side="left", padx=12, pady=6)

        self.lbl_precio_promo = ctk.CTkLabel(
            self.frame_precios_detalle,
            text="Precio promo: $0.00",
            font=("Arial", 12, "bold"),
            text_color="#FFFFFF"
        )
        self.lbl_precio_promo.pack(side="left", padx=15, pady=6)

        self.lbl_ahorro_promo = ctk.CTkLabel(
            self.frame_precios_detalle,
            text="Ahorro: $0.00",
            font=("Arial", 12, "bold"),
            text_color="#4ADE80"
        )
        self.lbl_ahorro_promo.pack(side="right", padx=12, pady=6)

        # 4. TABLA GENERAL DE PROMOCIONES REGISTRADAS
        self.card_tabla = ctk.CTkFrame(self.derecha, fg_color="#2B2B2B", corner_radius=10)
        self.card_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 12))

        self.header_tabla = ctk.CTkFrame(self.card_tabla, fg_color="#1F2937", corner_radius=6)
        self.header_tabla.pack(fill="x", padx=10, pady=(10, 4))

        ctk.CTkLabel(self.header_tabla, text="Promoción", font=("Arial", 12, "bold"), width=140, anchor="w").pack(side="left", padx=8, pady=5)
        ctk.CTkLabel(self.header_tabla, text="Productos incluidos", font=("Arial", 12, "bold"), anchor="w").pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ctk.CTkLabel(self.header_tabla, text="Precio", font=("Arial", 12, "bold"), width=80, anchor="e").pack(side="left", padx=8, pady=5)
        ctk.CTkLabel(self.header_tabla, text="Estado", font=("Arial", 12, "bold"), width=90, anchor="center").pack(side="left", padx=8, pady=5)

        self.lista_promociones = ctk.CTkScrollableFrame(self.card_tabla, fg_color="transparent")
        self.lista_promociones.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.cargar_promociones()

    def crear_kpi(self, parent, col, titulo, valor, color):
        card = ctk.CTkFrame(parent, fg_color="#2B2B2B", corner_radius=8)
        card.grid(row=0, column=col, sticky="nsew", padx=4)

        borde = ctk.CTkFrame(card, width=4, fg_color=color, corner_radius=3)
        borde.pack(side="left", fill="y", padx=(6, 8), pady=8)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=6, padx=(0, 6))

        ctk.CTkLabel(info, text=titulo, font=("Arial", 11, "bold"), text_color="#A1A1AA").pack(anchor="w")
        lbl_val = ctk.CTkLabel(info, text=valor, font=("Arial", 18, "bold"), text_color="#FFFFFF")
        lbl_val.pack(anchor="w")
        return lbl_val

    def refrescar_listas(self):
        """Actualiza automáticamente el panel al volver a entrar desde el menú"""
        self.cargar_promociones()

    def cancelar(self):
        self.codigos_promo.clear()
        self.productos_promo.clear()
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
        """Asigna secuencialmente hasta 3 productos compatibles y desbloquea su campo de cantidad"""
        if self.tproductobox.get().strip():
            messagebox.showinfo("Límite alcanzado", "Ya seleccionaste los 3 productos permitidos para la promoción.")
            return

        def al_elegir(codigo):
            prod = obtener_detalle_producto(codigo)
            if not prod:
                messagebox.showerror("Error", "No se pudo obtener la información del producto.")
                return

            compatible, motivo = self.es_producto_compatible(prod)
            if not compatible:
                messagebox.showwarning("Producto incompatible", motivo)
                return

            texto_mostrar = f"{codigo} - {prod['nombre']}"
            self.codigos_promo.append(codigo)
            self.productos_promo.append(prod)

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

    def obtener_resumen_paquete(self, promo):
        """Arma la lista legible de productos y calcula el precio regular del paquete"""
        partes = []
        precio_regular = 0.0

        slots = [
            (promo.get("fproducto"), promo.get("fcantidad"), promo.get("nombre_p1"), promo.get("precio_p1")),
            (promo.get("sproducto"), promo.get("scantidad"), promo.get("nombre_p2"), promo.get("precio_p2")),
            (promo.get("tproducto"), promo.get("tcantidad"), promo.get("nombre_p3"), promo.get("precio_p3")),
        ]

        for cod, cant, nom, p_unit in slots:
            if cod and cant:
                cant_int = int(cant)
                etiqueta = nom if nom else str(cod)
                partes.append(f"{cant_int}x {etiqueta}")
                precio_regular += cant_int * float(p_unit or 0)

        return " + ".join(partes) if partes else "Sin productos", precio_regular

    def actualizar_kpis(self):
        total = len(self.mapa_promociones)
        activas = sum(1 for p in self.mapa_promociones.values() if p.get("activo") == 1)
        inactivas = total - activas

        self.lbl_total_promos.configure(text=str(total))
        self.lbl_activas_promos.configure(text=str(activas))
        self.lbl_inactivas_promos.configure(text=str(inactivas))

    def cargar_promociones(self):
        """Consulta MySQL, actualiza contadores, ComboBox y tabla general"""
        seleccion_previa = self.combobox.get()
        promos = obtener_promociones_completas()
        self.mapa_promociones.clear()

        nombres = []
        for p in promos:
            nombre = p["nombre"]
            self.mapa_promociones[nombre] = p
            nombres.append(nombre)

        self.actualizar_kpis()
        self.renderizar_tabla_promociones(promos)

        if nombres:
            self.combobox.configure(values=nombres)
            if seleccion_previa in self.mapa_promociones:
                self.combobox.set(seleccion_previa)
                self.al_seleccionar_promo(seleccion_previa)
            else:
                self.combobox.set("Selecciona una promoción")
                self.limpiar_detalle()
        else:
            self.combobox.configure(values=["Sin promociones"])
            self.combobox.set("Sin promociones")
            self.limpiar_detalle()

    def limpiar_detalle(self):
        self.switch_activo.deselect()
        self.switch_activo.configure(text="Desactivada", state="disabled")
        self.btn_eliminar.configure(state="disabled")
        self.lbl_detalle_productos.configure(
            text="Seleccione una promoción de la lista o del menú superior para ver su contenido."
        )
        self.lbl_precio_regular.configure(text="Precio regular: $0.00")
        self.lbl_precio_promo.configure(text="Precio promo: $0.00")
        self.lbl_ahorro_promo.configure(text="Ahorro: $0.00", text_color="#4ADE80")

    def al_seleccionar_promo(self, nombre_elegido):
        """Sincroniza el switch, botón eliminar y tarjeta de ahorro al elegir una promoción"""
        promo = self.mapa_promociones.get(nombre_elegido)
        if not promo:
            return

        self.combobox.set(nombre_elegido)
        self.switch_activo.configure(state="normal")
        self.btn_eliminar.configure(state="normal")

        if promo["activo"] == 1:
            self.switch_activo.select()
            self.switch_activo.configure(text="Activa")
        else:
            self.switch_activo.deselect()
            self.switch_activo.configure(text="Desactivada")

        resumen, precio_regular = self.obtener_resumen_paquete(promo)
        precio_promo = float(promo.get("precio") or 0)
        ahorro = precio_regular - precio_promo

        self.lbl_detalle_productos.configure(text=f"Incluye:  {resumen}")
        self.lbl_precio_regular.configure(text=f"Precio regular: ${precio_regular:,.2f}")
        self.lbl_precio_promo.configure(text=f"Precio promo: ${precio_promo:,.2f}")

        if ahorro > 0:
            self.lbl_ahorro_promo.configure(text=f"Ahorro: ${ahorro:,.2f}", text_color="#4ADE80")
        else:
            self.lbl_ahorro_promo.configure(text=f"Sin descuento (${ahorro:,.2f})", text_color="#FBBF24")

    def renderizar_tabla_promociones(self, promos):
        for w in self.lista_promociones.winfo_children():
            w.destroy()

        if not promos:
            ctk.CTkLabel(
                self.lista_promociones,
                text="Aún no hay promociones registradas.",
                font=("Arial", 12),
                text_color="#A1A1AA"
            ).pack(pady=20)
            return

        for promo in promos:
            fila = ctk.CTkFrame(self.lista_promociones, fg_color="#232323", corner_radius=6)
            fila.pack(fill="x", pady=3, padx=2)

            nombre = promo["nombre"]
            resumen, _ = self.obtener_resumen_paquete(promo)
            precio = float(promo.get("precio") or 0)
            activa = promo.get("activo") == 1

            lbl_nom = ctk.CTkLabel(fila, text=nombre, font=("Arial", 12, "bold"), width=140, anchor="w")
            lbl_nom.pack(side="left", padx=8, pady=6)

            lbl_res = ctk.CTkLabel(fila, text=resumen, font=("Arial", 11), text_color="#D4D4D8", anchor="w")
            lbl_res.pack(side="left", fill="x", expand=True, padx=5, pady=6)

            lbl_pre = ctk.CTkLabel(fila, text=f"${precio:,.2f}", font=("Arial", 12, "bold"), width=80, anchor="e")
            lbl_pre.pack(side="left", padx=8, pady=6)

            lbl_est = ctk.CTkLabel(
                fila,
                text="Activa" if activa else "Desactivada",
                font=("Arial", 11, "bold"),
                width=90,
                text_color="#4ADE80" if activa else "#F87171"
            )
            lbl_est.pack(side="left", padx=8, pady=6)

            # Permitir seleccionar la promoción al hacer clic en cualquier parte de la fila
            for widget in (fila, lbl_nom, lbl_res, lbl_pre, lbl_est):
                widget.bind("<Button-1>", lambda _e, n=nombre: self.al_seleccionar_promo(n))

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
            self.actualizar_kpis()
            self.renderizar_tabla_promociones(list(self.mapa_promociones.values()))
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_promo_actual(self):
        """Elimina la promoción seleccionada previa confirmación"""
        nombre_elegido = self.combobox.get()
        promo = self.mapa_promociones.get(nombre_elegido)
        if not promo:
            return

        if not messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente la promoción '{nombre_elegido}'?"):
            return

        exito, mensaje = eliminarpromocion(promo["id"])
        if exito:
            messagebox.showinfo("Eliminada", mensaje)
            self.cargar_promociones()
        else:
            messagebox.showerror("Error", mensaje)

    def es_producto_compatible(self, prod):
        """Valida si un producto puede agregarse a la promoción actual"""
        clave_nueva = prod.get("codigo") or prod.get("codigobarras")
        for existente in self.productos_promo:
            clave_ex = existente.get("codigo") or existente.get("codigobarras")
            if clave_nueva and clave_nueva == clave_ex:
                return False, (
                    f"El producto '{prod['nombre']}' ya fue agregado a esta promoción.\n"
                    "Si desea incluir más unidades, modifique su campo Cantidad."
                )

        requisito = str(prod.get("requisito") or "Ninguno").strip()
        categoria = str(prod.get("categoria") or "Sin limitaciones").strip()

        if requisito in ("Receta", "Identificación") or categoria == "Limitado":
            return False, (
                f"No se puede agregar '{prod['nombre']}' porque tiene restricción de venta "
                f"(Requisito: {requisito} | Categoría: {categoria}).\n\n"
                "Las promociones solo permiten productos compatibles sin limitaciones."
            )

        if self.productos_promo:
            base = self.productos_promo[0]
            req_base = str(base.get("requisito") or "Ninguno").strip()
            cat_base = str(base.get("categoria") or "Sin limitaciones").strip()
            if requisito != req_base or categoria != cat_base:
                return False, (
                    f"'{prod['nombre']}' ({requisito} / {categoria}) no es compatible con "
                    f"'{base['nombre']}' ({req_base} / {cat_base})."
                )

        return True, ""