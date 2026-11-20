import customtkinter as ctk
from tkinter import messagebox, END
from Conexion import guardar, buscartrabajador, obtener_trabajadores, obtener_datos_reportes, actualizartrabajador, eliminartrabajador

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    TIENE_MATPLOTLIB = True
except ImportError:
    TIENE_MATPLOTLIB = False

class FrameAgregar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Título superior del panel
        self.label_titulo = ctk.CTkLabel(
            self, 
            text="Panel de Administración (Usuarios y Reportes)", 
            font=("Arial", 18, "bold")
        )
        self.label_titulo.pack(pady=(15, 10))

        # Contenedor principal horizontal (Dividido en Izquierda y Derecha)
        self.contenedor_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_principal.pack(fill="both", expand=True, padx=15, pady=10)

        # ====================================================
        # COLUMNA IZQUIERDA: FORMULARIO DE REGISTRO
        # ====================================================
        self.frame_agregar = ctk.CTkScrollableFrame(self.contenedor_principal, width=320) 
        self.frame_agregar.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.lbagregar = ctk.CTkLabel(
            self.frame_agregar, 
            text="Registrar usuario", 
            font=("Arial", 15, "bold")
        )
        self.lbagregar.pack(pady=(15, 10), anchor="w", padx=15)
        self.lbframe2=ctk.CTkLabel(
            self.frame_agregar,
            text="Revisar la informacion de un trabajador",
            font=("Arial", 18, "bold")
            )
        self.lbframe2.pack(anchor="w", padx=15, pady=(15, 10))

        self.inelejir=ctk.CTkLabel(
            self.frame_agregar,
            text="Seleccione nombre:",
            font=("Arial", 12, "bold")
        )
        self.inelejir.pack(anchor="nw", pady=(0, 5), padx=15)
        self.innombre=ctk.CTkComboBox(self.frame_agregar, values=[""], width=380, command=self.actualizar_trabajador)
        self.innombre.pack(anchor="sw", pady=(0, 8), padx=15)

        # Entradas de texto alineadas a la izquierda (anchor="w")
        self.userbox = self.crear_campo("Agregue Username:")
        self.nombrebox = self.crear_campo("Agregar nombre:")
        self.telefonobox = self.crear_campo("Agregue teléfono:")
        self.rfcbox = self.crear_campo("Agregue RFC:")
        self.direccionbox = self.crear_campo("Agregue dirección:")
        self.estadobox = self.crear_campo("Agregue estado:")
        self.emailbox = self.crear_campo("Agregue email:")
        self.passwordbox = self.crear_campo("Agregue password:", es_password=True)

        # Rango (ComboBox)
        self.lbrango = ctk.CTkLabel(self.frame_agregar, text="Agregue rango:", font=("Arial", 11, "bold"))
        self.lbrango.pack(anchor="w", padx=15, pady=(2, 0))

        self.rangobox = ctk.CTkComboBox(
            self.frame_agregar,
            values=["admin", "ventas", "almacen"],
            width=280,
            fg_color="#242526",
            button_color="#3A3B3C",
            text_color="#E4E6EB"
        )
        self.rangobox.pack(anchor="w", padx=15, pady=(0, 12))
        self.rangobox.set("Seleccione Rango")

        # Botón de registro (Ahora está dentro de la columna izquierda y siempre visible)
        self.btn_crear_usuario = ctk.CTkButton(
            self.frame_agregar,
            text="Registrar Nuevo Empleado",
            fg_color="#199912",
            hover_color="#11680D",
            width=280,
            command=self.registrar
        )
        self.btn_crear_usuario.pack(anchor="w", padx=15, pady=2)

        self.btn_cancelar= ctk.CTkButton(
            self.frame_agregar,
            text="Cancelar",
            fg_color="#DA2C3E",
            hover_color="#62010A",
            width=280,
            command=self.cancelar
        )
        self.btn_cancelar.pack(anchor="w", padx=15, pady=2)

        self.btchange=ctk.CTkButton(
            self.frame_agregar,
            text="Cambiar informacion",
            fg_color="#2456D4",
            hover_color="#0F0DAA",
            text_color="#FEFEFE",
            width=280,
            command=self.cambiar
        )
        self.btchange.pack(anchor="w", padx=15, pady=2)
        self.btchange.configure(state="disabled")

        self.btdespedir=ctk.CTkButton(
            self.frame_agregar,
            text="Despedir",
            fg_color="#CC2525",
            hover_color="#5B0A0A",
            text_color="#ECE9E9",
            width=300,
            command=self.despedir
        )
        self.btdespedir.pack(anchor="nw", pady=2)

        # ====================================================
        # COLUMNA DERECHA: PANEL DE REPORTES Y MÉTRICAS
        # ====================================================
        self.frame_informacion = ctk.CTkFrame(self.contenedor_principal)
        self.frame_informacion.pack(side="left", fill="both", expand=True, padx=(5, 0))

        # Encabezado de Reportes + Botón Actualizar
        self.header_reportes = ctk.CTkFrame(self.frame_informacion, fg_color="transparent")
        self.header_reportes.pack(fill="x", padx=15, pady=(12, 8))

        self.ltitulo = ctk.CTkLabel(
            self.header_reportes,
            text="Reportes y Resumen General",
            font=("Arial", 18, "bold")
        )
        self.ltitulo.pack(side="left")

        self.btn_refrescar = ctk.CTkButton(
            self.header_reportes,
            text="Actualizar datos",
            width=130,
            height=30,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=("Arial", 12, "bold"),
            command=self.cargar_reportes
        )
        self.btn_refrescar.pack(side="right")

        # 1. TARJETAS KPI (Cuadrícula 2x2)
        self.grid_kpis = ctk.CTkFrame(self.frame_informacion, fg_color="transparent")
        self.grid_kpis.pack(fill="x", padx=12, pady=(0, 10))
        self.grid_kpis.grid_columnconfigure((0, 1), weight=1)

        self.lbl_kpi_entrados = self.crear_tarjeta_kpi(
            self.grid_kpis, 0, 0, "Productos que han entrado", "0", "#3B82F6"
        )
        self.lbl_kpi_vendidos = self.crear_tarjeta_kpi(
            self.grid_kpis, 0, 1, "Productos que han sido vendidos", "0", "#10B981"
        )
        self.lbl_kpi_ganancia = self.crear_tarjeta_kpi(
            self.grid_kpis, 1, 0, "Ganancia Neta / Estimada", "$0.00", "#F59E0B"
        )
        self.lbl_kpi_inventario = self.crear_tarjeta_kpi(
            self.grid_kpis, 1, 1, "Valor del Inventario (Costo)", "$0.00", "#8B5CF6"
        )

        # 2. SECCIÓN CENTRAL: GRÁFICA DE GANANCIAS
        self.card_grafica = ctk.CTkFrame(self.frame_informacion, fg_color="#2B2B2B", corner_radius=10)
        self.card_grafica.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.lgrafica = ctk.CTkLabel(
            self.card_grafica,
            text="Gráfica de ganancias por producto (Costo vs. Ganancia)",
            font=("Arial", 13, "bold")
        )
        self.lgrafica.pack(anchor="w", padx=12, pady=(8, 4))

        self.contenedor_grafica = ctk.CTkFrame(self.card_grafica, fg_color="transparent")
        self.contenedor_grafica.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        # 3. SECCIÓN INFERIOR: ALERTA DE STOCK BAJO
        self.card_stock = ctk.CTkFrame(self.frame_informacion, fg_color="#2B2B2B", corner_radius=10, height=150)
        self.card_stock.pack(fill="x", padx=15, pady=(0, 12))

        self.lgrafica = ctk.CTkLabel(
            self.card_grafica,
            text="Gráfica de ganancias por producto (Costo vs. Ganancia)",
            font=("Arial", 13, "bold")
        )
        self.lgrafica.pack(anchor="w", padx=12, pady=(8, 4))

        self.contenedor_grafica = ctk.CTkFrame(self.card_grafica, fg_color="transparent")
        self.contenedor_grafica.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        # 3. SECCIÓN INFERIOR: ALERTA DE STOCK BAJO
        self.card_stock = ctk.CTkFrame(self.frame_informacion, fg_color="#2B2B2B", corner_radius=10, height=150)
        self.card_stock.pack(fill="x", padx=15, pady=(0, 12))
        self.card_stock.pack_propagate(False)

        self.lbl_stock_titulo = ctk.CTkLabel(
            self.card_stock,
            text="Alerta: Productos próximos a agotarse (Stock ≤ 5)",
            font=("Arial", 13, "bold"),
            text_color="#F87171"
        )
        self.lbl_stock_titulo.pack(anchor="w", padx=12, pady=(8, 4))

        self.lista_bajo_stock = ctk.CTkScrollableFrame(self.card_stock, fg_color="#232323", corner_radius=6)
        self.lista_bajo_stock.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        self.cargar_reportes()
        
    def crear_campo(self, texto_label, es_password=False):
        """Método auxiliar para crear etiqueta + entrada alineados a la izquierda"""
        lbl = ctk.CTkLabel(self.frame_agregar, text=texto_label, font=("Arial", 11, "bold"))
        lbl.pack(anchor="w", padx=15, pady=(2, 0))

        if es_password:
            entry = ctk.CTkEntry(self.frame_agregar, show="*", width=280)
        else:
            entry = ctk.CTkEntry(self.frame_agregar, width=280)

        entry.pack(anchor="w", padx=15, pady=(0, 4))
        return entry

    def registrar(self):
        username = self.userbox.get().strip()
        nombre = self.nombrebox.get().strip()
        telefono = self.telefonobox.get().strip()
        rfc = self.rfcbox.get().strip()
        direccion = self.direccionbox.get().strip()
        estado = self.estadobox.get().strip()
        email = self.emailbox.get().strip()
        password = self.passwordbox.get().strip()
        rango = self.rangobox.get().strip()

        if rango == "Seleccione Rango" or rango not in ["admin", "ventas", "almacen"]:
            messagebox.showerror("Error", "Por favor seleccione un rango válido.")
            return

        if not all([username, nombre, telefono, rfc, direccion, estado, email, password, rango]):
            messagebox.showerror("Error", "Datos incompletos.")
            return

        exito, mensaje = guardar(username, nombre, telefono, rfc, direccion, estado, email, password, rango)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
        else:
            messagebox.showerror("Error", mensaje)

    def cancelar(self):
        self.trabajador_actual_id = None

        cajas = [
            self.userbox, self.nombrebox, self.telefonobox, self.rfcbox,
            self.direccionbox, self.estadobox, self.emailbox, self.passwordbox
        ]
        for caja in cajas:
            caja.configure(state="normal")
            caja.delete(0, END)

        self.innombre.set("")
        self.rangobox.configure(state="normal")
        self.rangobox.set("Seleccione Rango")

        # Restaurar botones a su estado inicial
        self.btn_crear_usuario.configure(state="normal")
        self.btchange.configure(
            text="Cambiar informacion",
            fg_color="#2456D4",
            hover_color="#0F0DAA",
            command=self.cambiar,
            state="disabled"
        )

    def cargar_trabajadores(self):
        trabajadores = obtener_trabajadores()
        nombres = [t["nombre"] for t in trabajadores if t.get("nombre")]
        self.innombre.configure(values=nombres if nombres else [""])
        self.innombre.set("")

    def actualizar_trabajador(self, _seleccion=None):
        trabajador = self.innombre.get().strip()
        if not trabajador:
            return

        datos = buscartrabajador(trabajador)
        if not datos:
            messagebox.showwarning("Sin resultados", "No se encontró el trabajador")
            return

        self.trabajador_actual_id = datos["userid"]
        self.btchange.configure(state="normal")

        campos = [
            (self.userbox, datos["username"] or ""),
            (self.nombrebox, datos["nombre"] or ""),
            (self.telefonobox, datos["telefono"] or ""),
            (self.rfcbox, datos["rfc"] or ""),
            (self.direccionbox, datos["direccion"] or ""),
            (self.estadobox, datos["estado"] or ""),
            (self.emailbox, datos["email"] or ""),
            (self.passwordbox, "**************"),
        ]

        for caja, valor in campos:
            caja.configure(state="normal")
            caja.delete(0, END)
            caja.insert(0, valor)
            caja.configure(state="disabled")

        self.rangobox.set(datos["rango"] or "Seleccione Rango")
        self.rangobox.configure(state="disabled")

#########################boton de informacion

    def cambiar(self):
        """Habilita los campos del trabajador seleccionado para editarlos"""
        if not getattr(self, "trabajador_actual_id", None):
            messagebox.showwarning("Advertencia", "Primero seleccione un trabajador de la lista.")
            return

        cajas = [
            self.userbox, self.nombrebox, self.telefonobox, self.rfcbox,
            self.direccionbox, self.estadobox, self.emailbox
        ]
        for caja in cajas:
            caja.configure(state="normal")

        # Vaciar los asteriscos; si se deja en blanco conserva la contraseña actual
        self.passwordbox.configure(state="normal")
        self.passwordbox.delete(0, END)

        self.rangobox.configure(state="normal")

        # Bloquear registro nuevo mientras se edita y convertir el botón en Guardar cambios
        self.btn_crear_usuario.configure(state="disabled")
        self.btchange.configure(
            text="Guardar cambios",
            fg_color="#D97706",
            hover_color="#B45309",
            command=self.guardarcambios
        )
        messagebox.showinfo(
            "Modo edición",
            "Campos desbloqueados.\nModifique los datos necesarios y presione 'Guardar cambios'.\n(Deje la contraseña vacía si no desea cambiarla)."
        )
    def despedir(self):
        """Elimina al trabajador seleccionado previa confirmación"""
        if not getattr(self, "trabajador_actual_id", None):
            messagebox.showwarning("Sin selección", "Primero seleccione un trabajador de la lista.")
            return

        nombre = self.nombrebox.get().strip() or self.innombre.get().strip()
        confirmar = messagebox.askyesno(
            "Confirmar despido",
            f"¿Está seguro de despedir y eliminar del sistema a '{nombre}'?\n\nEsta acción no se puede deshacer."
        )
        if not confirmar:
            return

        exito, mensaje = eliminartrabajador(self.trabajador_actual_id)
        if exito:
            messagebox.showinfo("Baja completada", mensaje)
            self.cancelar()
            self.cargar_trabajadores()
        else:
            messagebox.showerror("Error", mensaje)
    def guardarcambios(self):
        """Guarda en MySQL las modificaciones hechas al trabajador"""
        if not getattr(self, "trabajador_actual_id", None):
            messagebox.showerror("Error", "No hay ningún trabajador seleccionado para actualizar.")
            return

        username = self.userbox.get().strip()
        nombre = self.nombrebox.get().strip()
        telefono = self.telefonobox.get().strip()
        rfc = self.rfcbox.get().strip()
        direccion = self.direccionbox.get().strip()
        estado = self.estadobox.get().strip()
        email = self.emailbox.get().strip()
        password = self.passwordbox.get().strip()
        rango = self.rangobox.get().strip()

        if password == "**************":
            password = ""

        if rango == "Seleccione Rango" or rango not in ["admin", "ventas", "almacen"]:
            messagebox.showerror("Error", "Por favor seleccione un rango válido.")
            return

        if not all([username, nombre, telefono, rfc, direccion, estado, email, rango]):
            messagebox.showerror("Error", "Complete todos los campos obligatorios.")
            return

        exito, mensaje = actualizartrabajador(
            self.trabajador_actual_id,
            username,
            nombre,
            telefono,
            rfc,
            direccion,
            estado,
            email,
            password,
            rango
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
            self.cargar_trabajadores()
        else:
            messagebox.showerror("Error", mensaje)

    def crear_tarjeta_kpi(self, parent, fila, columna, titulo, valor_inicial, color_acento):
        tarjeta = ctk.CTkFrame(parent, fg_color="#2B2B2B", corner_radius=10)
        tarjeta.grid(row=fila, column=columna, sticky="nsew", padx=5, pady=5)

        barra = ctk.CTkFrame(tarjeta, width=5, fg_color=color_acento, corner_radius=4)
        barra.pack(side="left", fill="y", padx=(8, 10), pady=10)

        contenido = ctk.CTkFrame(tarjeta, fg_color="transparent")
        contenido.pack(side="left", fill="both", expand=True, pady=8, padx=(0, 10))

        lbl_tit = ctk.CTkLabel(
            contenido,
            text=titulo,
            font=("Arial", 11, "bold"),
            text_color="#A1A1AA"
        )
        lbl_tit.pack(anchor="w")

        lbl_val = ctk.CTkLabel(
            contenido,
            text=valor_inicial,
            font=("Arial", 20, "bold"),
            text_color="#FFFFFF"
        )
        lbl_val.pack(anchor="w", pady=(2, 0))
        return lbl_val

    def refrescar_listas(self):
        """Se ejecuta automáticamente al entrar a Administración desde usuario.py"""
        self.cargar_trabajadores()
        self.cargar_reportes()

    def cargar_reportes(self):
        datos = obtener_datos_reportes()

        self.lbl_kpi_entrados.configure(text=str(datos["entrados"]))
        self.lbl_kpi_vendidos.configure(text=str(datos["vendidos"]))
        self.lbl_kpi_ganancia.configure(text=f"${datos['ganancia_total']:,.2f}")
        self.lbl_kpi_inventario.configure(text=f"${datos['valor_inventario']:,.2f}")

        self.dibujar_grafica(datos["grafica"])
        self.renderizar_bajo_stock(datos["bajo_stock"])

    def dibujar_grafica(self, items):
        for w in self.contenedor_grafica.winfo_children():
            w.destroy()

        if not items:
            ctk.CTkLabel(
                self.contenedor_grafica,
                text="Registre productos para visualizar la gráfica de ganancias.",
                font=("Arial", 12),
                text_color="#A1A1AA"
            ).pack(expand=True)
            return

        nombres = [str(p["nombre"])[:12] for p in items]
        costos = [float(p["costo"] or 0) for p in items]
        ganancias = [max(0.0, float(p["ganancia"] or 0)) for p in items]

        if TIENE_MATPLOTLIB:
            fig = Figure(figsize=(5.5, 2.4), dpi=95, facecolor="#2B2B2B")
            ax = fig.add_subplot(111)
            ax.set_facecolor("#232323")

            x = range(len(nombres))
            ancho = 0.36
            ax.bar([i - ancho / 2 for i in x], costos, width=ancho, label="Costo", color="#3B82F6")
            ax.bar([i + ancho / 2 for i in x], ganancias, width=ancho, label="Ganancia", color="#10B981")

            ax.set_xticks(list(x))
            ax.set_xticklabels(nombres, color="#E4E4E7", fontsize=8)
            ax.tick_params(axis="y", colors="#E4E4E7", labelsize=8)
            for spine in ax.spines.values():
                spine.set_color("#3F3F46")
            ax.legend(facecolor="#2B2B2B", edgecolor="none", labelcolor="#FFFFFF", fontsize=8)
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.contenedor_grafica)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            canvas = ctk.CTkCanvas(self.contenedor_grafica, bg="#232323", highlightthickness=0)
            canvas.pack(fill="both", expand=True)

            def pintar(_event=None):
                canvas.delete("all")
                w = max(canvas.winfo_width(), 300)
                h = max(canvas.winfo_height(), 150)
                max_val = max(max(costos + ganancias), 1.0)
                n = len(nombres)
                paso = (w - 40) / max(n, 1)

                for i in range(n):
                    cx = 25 + i * paso + paso / 2
                    h_costo = (costos[i] / max_val) * (h - 50)
                    h_gan = (ganancias[i] / max_val) * (h - 50)

                    canvas.create_rectangle(cx - 18, h - 25 - h_costo, cx - 2, h - 25, fill="#3B82F6", outline="")
                    canvas.create_rectangle(cx + 2, h - 25 - h_gan, cx + 18, h - 25, fill="#10B981", outline="")
                    canvas.create_text(cx, h - 12, text=nombres[i], fill="#E4E4E7", font=("Arial", 8))

                canvas.create_text(55, 12, text="■ Costo", fill="#3B82F6", font=("Arial", 9, "bold"))
                canvas.create_text(130, 12, text="■ Ganancia", fill="#10B981", font=("Arial", 9, "bold"))

            canvas.bind("<Configure>", pintar)

    def renderizar_bajo_stock(self, lista):
        for w in self.lista_bajo_stock.winfo_children():
            w.destroy()

        if not lista:
            ctk.CTkLabel(
                self.lista_bajo_stock,
                text="Todo el inventario cuenta con existencias suficientes.",
                font=("Arial", 12),
                text_color="#4ADE80"
            ).pack(pady=10)
            return

        for prod in lista:
            fila = ctk.CTkFrame(self.lista_bajo_stock, fg_color="transparent")
            fila.pack(fill="x", padx=6, pady=2)

            ctk.CTkLabel(
                fila,
                text=f"[{prod['codigo']}]  {prod['nombre']}",
                font=("Arial", 12)
            ).pack(side="left")

            ctk.CTkLabel(
                fila,
                text=f"Stock: {prod['stock']}",
                font=("Arial", 12, "bold"),
                text_color="#F87171"
            ).pack(side="right")