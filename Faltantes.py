import os
import re
import customtkinter as ctk
from tkinter import messagebox, END
from Busquda import VentanaBusqueda, VentanaBusquedaProveedor
from ListaFaltantes import listafaltantes
from Conexion import obtener_producto_con_proveedor, buscarprovedor


class FrameFaltantes(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.lista_productos = []
        self.producto_actual = None
        self.filtro_proveedor_id = None
        self.filtro_proveedor_nombre = ""

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        # ====================================================
        # 1. TRES BLOQUES VERTICALES PRINCIPALES
        # ====================================================
        self.arriba = ctk.CTkFrame(self.contenedor)
        self.arriba.pack(side="top", fill="both", expand=True, pady=(0, 10))

        self.medio = ctk.CTkFrame(self.contenedor, height=90)
        self.medio.pack(side="top", fill="x", pady=(0, 10))

        self.comandos = ctk.CTkFrame(self.contenedor, height=70)
        self.comandos.pack(side="top", fill="x")

        # ====================================================
        # 2. CONTENIDO DEL BLOQUE SUPERIOR (TABLA EN 4 SECCIONES)
        # ====================================================
        self.lbtutulo = ctk.CTkLabel(
            self.arriba,
            text="Almacén / Faltantes",
            font=("Arial", 22, "bold")
        )
        self.lbtutulo.pack(side="top", pady=(15, 10))

        # Contenedor para las 4 columnas
        self.frame_columnas = ctk.CTkFrame(self.arriba, fg_color="transparent")
        self.frame_columnas.pack(side="top", fill="both", expand=True, padx=15, pady=(0, 15))

        # Configuración del GRID (0: Código, 1: Cantidad, 2: Detalles, 3: Proveedor)
        self.frame_columnas.grid_columnconfigure(0, weight=1)
        self.frame_columnas.grid_columnconfigure(1, weight=1)
        self.frame_columnas.grid_columnconfigure(2, weight=2)
        self.frame_columnas.grid_columnconfigure(3, weight=1)
        self.frame_columnas.grid_rowconfigure(0, weight=1)

        # SECCIÓN 1: CÓDIGO
        self.codigoframe = ctk.CTkScrollableFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.codigoframe.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.lcodigo = ctk.CTkLabel(self.codigoframe, text="Código", font=("Arial", 16, "bold"))
        self.lcodigo.pack(pady=10)

        # SECCIÓN 2: CANTIDAD
        self.cantidadframe = ctk.CTkScrollableFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.cantidadframe.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.lcantidad = ctk.CTkLabel(self.cantidadframe, text="Cantidad", font=("Arial", 16, "bold"))
        self.lcantidad.pack(pady=10)

        # SECCIÓN 3: DETALLES
        self.detallesframe = ctk.CTkScrollableFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.detallesframe.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.ldetalles = ctk.CTkLabel(self.detallesframe, text="Detalles", font=("Arial", 16, "bold"))
        self.ldetalles.pack(pady=10)

        # SECCIÓN 4: PROVEEDOR
        self.proveedorframe = ctk.CTkScrollableFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.proveedorframe.grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

        self.lproveedor = ctk.CTkLabel(self.proveedorframe, text="Proveedor", font=("Arial", 16, "bold"))
        self.lproveedor.pack(pady=10)

        # ====================================================
        # 3. BLOQUE MEDIO (FORMULARIO DE CAPTURA)
        # ====================================================
        self.frame_medio_inner = ctk.CTkFrame(self.medio, fg_color="transparent")
        self.frame_medio_inner.pack(fill="both", expand=True, padx=10, pady=10)

        # Campo 1: Proveedor (se detecta automáticamente al cargar el producto)
        self.f_prov = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_prov.pack(side="left", padx=5)
        self.blprovedor = ctk.CTkLabel(self.f_prov, text="Proveedor:", font=("Arial", 11, "bold"))
        self.blprovedor.pack(anchor="w")
        self.blprovedorbox = ctk.CTkEntry(self.f_prov, width=160)
        self.blprovedorbox.pack(pady=(2, 0))
        self.blprovedorbox.configure(state="disabled")

        # Campo 2: Código
        self.f_cod = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_cod.pack(side="left", padx=5)
        self.blcodigo = ctk.CTkLabel(self.f_cod, text="Código del producto:", font=("Arial", 11, "bold"))
        self.blcodigo.pack(anchor="w")
        self.blcodigobox = ctk.CTkEntry(self.f_cod, width=130)
        self.blcodigobox.pack(pady=(2, 0))

        # Campo 3: Cantidad
        self.f_cant = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_cant.pack(side="left", padx=5)
        self.blcantidad = ctk.CTkLabel(self.f_cant, text="Cantidad:", font=("Arial", 11, "bold"))
        self.blcantidad.pack(anchor="w")
        self.blcantidadbox = ctk.CTkEntry(self.f_cant, width=110)
        self.blcantidadbox.pack(pady=(2, 0))

        # Campo 4: Detalles
        self.f_det = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_det.pack(side="left", fill="x", expand=True, padx=5)
        self.bldetalles = ctk.CTkLabel(self.f_det, text="Detalles del producto:", font=("Arial", 11, "bold"))
        self.bldetalles.pack(anchor="w")
        self.bldetallesbox = ctk.CTkEntry(self.f_det)
        self.bldetallesbox.pack(fill="x", pady=(2, 0))
        self.bldetallesbox.configure(state="disabled")

        # Botones de Acción
        self.f_btns = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_btns.pack(side="right", padx=(10, 5), pady=(18, 0))

        self.btsubir = ctk.CTkButton(
            self.f_btns,
            text="Subir",
            fg_color="#2DE02D",
            hover_color="#187F18",
            text_color="#000000",
            width=65,
            font=("Arial", 12, "bold"),
            command=self.subir
        )
        self.btsubir.pack(side="left", padx=3)

        self.btcancelar = ctk.CTkButton(
            self.f_btns,
            text="Cancelar",
            fg_color="#E02D2D",
            hover_color="#981616",
            width=65,
            font=("Arial", 12, "bold"),
            command=self.cancelar
        )
        self.btcancelar.pack(side="left", padx=3)

        self.btenter = ctk.CTkButton(
            self.f_btns,
            text="Enter",
            fg_color="#325CE2",
            hover_color="#162E98",
            width=65,
            font=("Arial", 12, "bold"),
            command=self.enter
        )
        self.btenter.pack(side="left", padx=3)

        # ====================================================
        # 4. BLOQUE COMANDOS (TECLAS DE ATAJO)
        # ====================================================
        self.frame_cmd_inner = ctk.CTkFrame(self.comandos, fg_color="transparent")
        self.frame_cmd_inner.pack(fill="both", expand=True, padx=15, pady=12)

        # --- F1 (Filtro opcional por proveedor) ---
        self.item_f1 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f1.pack(side="left", padx=(0, 30))

        self.f1 = ctk.CTkButton(
            self.item_f1,
            text="F1",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=45,
            height=28,
            font=("Arial", 12, "bold"),
            command=self.busquedaprovedor
        )
        self.f1.pack(side="left", padx=(0, 8))

        self.lf1 = ctk.CTkLabel(self.item_f1, text="Filtrar Proveedor", font=("Arial", 12, "bold"))
        self.lf1.pack(side="left")

        # --- F2 (Buscar en todos los productos o del proveedor filtrado) ---
        self.item_f2 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f2.pack(side="left", padx=30)

        self.f2 = ctk.CTkButton(
            self.item_f2,
            text="F2",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=45,
            height=28,
            font=("Arial", 12, "bold"),
            command=self.busquedacodigo
        )
        self.f2.pack(side="left", padx=(0, 8))

        self.lf2 = ctk.CTkLabel(self.item_f2, text="Buscar Producto", font=("Arial", 12, "bold"))
        self.lf2.pack(side="left")

        # --- F3 ---
        self.item_f3 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f3.pack(side="left", padx=30)

        self.f3 = ctk.CTkButton(
            self.item_f3,
            text="F3",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=45,
            height=28,
            font=("Arial", 12, "bold"),
            command=self.borrarproducto
        )
        self.f3.pack(side="left", padx=(0, 8))

        self.lf3 = ctk.CTkLabel(self.item_f3, text="Cancelar Producto", font=("Arial", 12, "bold"))
        self.lf3.pack(side="left")

        # --- F4 ---
        self.item_f4 = ctk.CTkFrame(self.frame_cmd_inner, fg_color="transparent")
        self.item_f4.pack(side="left", padx=30)

        self.f4 = ctk.CTkButton(
            self.item_f4,
            text="F4",
            fg_color="#FFFFFF",
            hover_color="#E0E0E0",
            text_color="#000000",
            width=45,
            height=28,
            font=("Arial", 12, "bold"),
            command=self.subirsistema
        )
        self.f4.pack(side="left", padx=(0, 8))

        self.lf4 = ctk.CTkLabel(self.item_f4, text="Subir al sistema", font=("Arial", 12, "bold"))
        self.lf4.pack(side="left")

        # Atajos de teclado
        self.blcodigobox.bind("<Return>", self.enter)
        self.blcantidadbox.bind("<Return>", self.enter)

        root = self.winfo_toplevel()
        root.bind("<F1>", lambda e: self.busquedaprovedor() if self.winfo_ismapped() else None, add="+")
        root.bind("<F2>", lambda e: self.busquedacodigo() if self.winfo_ismapped() else None, add="+")
        root.bind("<F3>", lambda e: self.borrarproducto() if self.winfo_ismapped() else None, add="+")
        root.bind("<F4>", lambda e: self.subirsistema() if self.winfo_ismapped() else None, add="+")

    # ====================================================
    # LÓGICA DE EVENTOS Y ACCIONES
    # ====================================================
    def busquedaprovedor(self):
        """Filtro opcional (F1): si se elige un proveedor, F2 solo mostrará sus productos hasta presionar Cancelar"""
        def al_elegir(prov):
            self.filtro_proveedor_id = prov.get("id")
            self.filtro_proveedor_nombre = prov.get("nombre", "")

            self.blprovedorbox.configure(state="normal")
            self.blprovedorbox.delete(0, END)
            self.blprovedorbox.insert(0, f"Filtro: {self.filtro_proveedor_nombre}")
            self.blprovedorbox.configure(state="disabled")
            self.blcodigobox.focus()

        VentanaBusquedaProveedor(self, al_seleccionar_callback=al_elegir)

    def busquedacodigo(self):
        """Abre el buscador general de productos (o filtrado si se usó F1)"""
        def al_elegir(codigo):
            self.blcodigobox.delete(0, END)
            self.blcodigobox.insert(0, codigo)
            self.enter()

        VentanaBusqueda(
            self,
            al_seleccionar_callback=al_elegir,
            modo="faltantes",
            id_proveedor=self.filtro_proveedor_id
        )

    def cancelar(self):
        """Limpia las cajas del formulario y quita cualquier filtro de proveedor"""
        self.producto_actual = None
        self.filtro_proveedor_id = None
        self.filtro_proveedor_nombre = ""

        self.blprovedorbox.configure(state="normal")
        self.blprovedorbox.delete(0, END)
        self.blprovedorbox.configure(state="disabled")

        self.blcodigobox.delete(0, END)
        self.blcantidadbox.delete(0, END)

        self.bldetallesbox.configure(state="normal")
        self.bldetallesbox.delete(0, END)
        self.bldetallesbox.configure(state="disabled")
        self.blcodigobox.focus()

    def borrarproducto(self):
        """Limpia solo la captura del producto actual (F3), conservando el filtro si existe"""
        self.producto_actual = None
        self.blcodigobox.delete(0, END)
        self.blcantidadbox.delete(0, END)

        self.bldetallesbox.configure(state="normal")
        self.bldetallesbox.delete(0, END)
        self.bldetallesbox.configure(state="disabled")

        self.blprovedorbox.configure(state="normal")
        self.blprovedorbox.delete(0, END)
        if self.filtro_proveedor_nombre:
            self.blprovedorbox.insert(0, f"Filtro: {self.filtro_proveedor_nombre}")
        self.blprovedorbox.configure(state="disabled")
        self.blcodigobox.focus()

    def renderizar_tabla(self):
        """Dibuja las 4 columnas (Código, Cantidad, Detalles, Proveedor) desde self.lista_productos"""
        columnas = [self.codigoframe, self.cantidadframe, self.detallesframe, self.proveedorframe]

        for frame in columnas:
            widgets = frame.winfo_children()
            for w in widgets[1:]:
                w.destroy()

        for p in self.lista_productos:
            ctk.CTkLabel(self.codigoframe, text=p["codigo"], font=("Arial", 12)).pack(pady=2)
            ctk.CTkLabel(self.cantidadframe, text=str(p["cantidad"]), font=("Arial", 12)).pack(pady=2)
            ctk.CTkLabel(self.detallesframe, text=p["detalles"], font=("Arial", 12)).pack(pady=2)
            ctk.CTkLabel(self.proveedorframe, text=p["proveedor"], font=("Arial", 12, "bold"), text_color="#60A5FA").pack(pady=2)

    def enter(self, event=None):
        """Busca el producto en toda la base de datos y muestra automáticamente su proveedor y detalles"""
        codigo = self.blcodigobox.get().strip()
        if not codigo:
            return

        try:
            cantidad = int(self.blcantidadbox.get().strip())
            if cantidad <= 0:
                messagebox.showerror("Error", "No se permiten cantidades negativas o cero.")
                return
        except ValueError:
            cantidad = 1
            self.blcantidadbox.delete(0, END)
            self.blcantidadbox.insert(0, str(cantidad))

        producto = obtener_producto_con_proveedor(codigo)
        if not producto:
            messagebox.showerror("No encontrado", f"El producto '{codigo}' no existe en la base de datos.")
            return

        if self.filtro_proveedor_id and str(producto.get("idprovedor")) != str(self.filtro_proveedor_id):
            messagebox.showwarning(
                "Proveedor distinto al filtro",
                f"Este producto pertenece a '{producto.get('nombre_proveedor')}', "
                f"pero tienes activo el filtro '{self.filtro_proveedor_nombre}'.\n\n"
                "Presione Cancelar si desea capturar productos de todos los proveedores."
            )
            return

        self.producto_actual = producto
        nombre = producto.get("nombre") or ""
        descripcion = producto.get("descripcion") or ""
        nombre_prov = producto.get("nombre_proveedor") or "Sin proveedor"
        texto_detalles = f"{nombre} - {descripcion}" if descripcion else nombre

        self.blprovedorbox.configure(state="normal")
        self.blprovedorbox.delete(0, END)
        self.blprovedorbox.insert(0, nombre_prov)
        self.blprovedorbox.configure(state="disabled")

        self.bldetallesbox.configure(state="normal")
        self.bldetallesbox.delete(0, END)
        self.bldetallesbox.insert(0, texto_detalles)
        self.bldetallesbox.configure(state="disabled")

    def subir(self):
        """Agrega el producto junto con su proveedor a la tabla"""
        codigo = self.blcodigobox.get().strip()
        detalles = self.bldetallesbox.get().strip()

        if not codigo or not detalles or not self.producto_actual:
            messagebox.showwarning("Advertencia", "Primero presione Enter para cargar los datos del producto.")
            return

        try:
            cantidad = int(self.blcantidadbox.get().strip())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                return
        except ValueError:
            cantidad = 1

        nombre_prov = self.producto_actual.get("nombre_proveedor") or "Sin proveedor"
        id_prov = self.producto_actual.get("idprovedor")

        for item in self.lista_productos:
            if item["codigo"] == codigo:
                item["cantidad"] += cantidad
                self.renderizar_tabla()
                self.borrarproducto()
                return

        self.lista_productos.append({
            "codigo": codigo,
            "cantidad": cantidad,
            "detalles": detalles,
            "id_proveedor": id_prov,
            "proveedor": nombre_prov
        })

        self.renderizar_tabla()
        self.borrarproducto()

    def subirsistema(self):
        """Separa los productos por proveedor y genera un archivo .txt independiente por cada uno (F4)"""
        if not self.lista_productos:
            messagebox.showwarning("Lista vacía", "Agregue al menos un producto a la tabla antes de subir.")
            return

        # Agrupar productos por nombre de proveedor conservando el orden
        grupos_por_proveedor = {}
        for item in self.lista_productos:
            prov = item.get("proveedor") or "Sin_Proveedor"
            grupos_por_proveedor.setdefault(prov, []).append(item)

        try:
            proveedores_generados = []
            for nombre_prov, productos_prov in grupos_por_proveedor.items():
                listafaltantes(nombre_prov, productos_prov)
                proveedores_generados.append(f"• {nombre_prov} ({len(productos_prov)} prod.)")

            self.lista_productos.clear()
            self.renderizar_tabla()
            self.cancelar()

            resumen = "\n".join(proveedores_generados)
            messagebox.showinfo(
                "Listas generadas",
                f"Se separaron y guardaron las listas de faltantes por proveedor:\n\n{resumen}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron generar los archivos de faltantes: {e}")

    def cargar_desde_txt(self, ruta_archivo):
        """Lee un archivo .txt de faltantes y despliega sus productos con su proveedor en la tabla"""
        if not os.path.exists(ruta_archivo):
            return

        nombre_prov = ""
        productos_cargados = []

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    texto = linea.strip()
                    if not texto or texto.startswith(("=", "-", "Fecha:", "Total")):
                        continue

                    if texto.startswith("Proveedor:"):
                        nombre_prov = texto.replace("Proveedor:", "").strip()
                        continue

                    if texto.lower().startswith(("código", "codigo")) and ("cantidad" in texto.lower() or "detalles" in texto.lower()):
                        continue

                    separador = "|" if "|" in texto else ("\t" if "\t" in texto else None)
                    if separador:
                        partes = [p.strip() for p in texto.split(separador) if p.strip()]
                        if len(partes) >= 3:
                            cod = re.sub(r"^(Código|Codigo):\s*", "", partes[0], flags=re.IGNORECASE)
                            p1 = re.sub(r"^Cantidad:\s*", "", partes[1], flags=re.IGNORECASE)
                            p2 = re.sub(r"^Detalles:\s*", "", partes[2], flags=re.IGNORECASE)

                            if p1.isdigit():
                                cant, det = int(p1), p2
                            elif p2.isdigit():
                                det, cant = p1, int(p2)
                            else:
                                cant, det = 1, f"{p1} - {p2}"

                            productos_cargados.append({
                                "codigo": cod,
                                "cantidad": cant,
                                "detalles": det,
                                "proveedor": nombre_prov
                            })
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la lista de faltantes: {e}")
            return

        if not nombre_prov:
            nombre_prov = os.path.basename(ruta_archivo).replace("Faltantes_", "").replace(".txt", "")

        datos_prov = buscarprovedor(nombre_prov)
        id_prov = datos_prov["id"] if datos_prov else None
        prov_final = datos_prov["nombre"] if datos_prov else nombre_prov

        for item in productos_cargados:
            item["id_proveedor"] = id_prov
            item["proveedor"] = prov_final

        self.lista_productos = productos_cargados
        self.renderizar_tabla()