import os
import re
import customtkinter as ctk
from tkinter import messagebox, END
from Busquda import VentanaBusqueda, VentanaBusquedaProveedor
from ListaFaltantes import listafaltantes
from Conexion import buscar_producto_por_codigo, obtener_producto_de_proveedor, obtener_nombre_proveedor, buscarprovedor

class FrameFaltantes(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.lista_productos = []
        self.nombre_proveedor = ""

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
        # 2. CONTENIDO DEL BLOQUE SUPERIOR (TABLA EN 3 SECCIONES)
        # ====================================================
        self.lbtutulo = ctk.CTkLabel(
            self.arriba,
            text="Almacén / Faltantes",
            font=("Arial", 22, "bold")
        )
        self.lbtutulo.pack(side="top", pady=(15, 10))

        # Contenedor para las 3 columnas
        self.frame_columnas = ctk.CTkFrame(self.arriba, fg_color="transparent")
        self.frame_columnas.pack(side="top", fill="both", expand=True, padx=15, pady=(0, 15))

        # Configuración del GRID (0: Código, 1: Cantidad, 2: Detalles)
        self.frame_columnas.grid_columnconfigure(0, weight=1)
        self.frame_columnas.grid_columnconfigure(1, weight=1)
        self.frame_columnas.grid_columnconfigure(2, weight=2)
        self.frame_columnas.grid_rowconfigure(0, weight=1)

        # SECCIÓN 1: CÓDIGO
        self.codigoframe = ctk.CTkScrollableFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.codigoframe.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.lcodigo = ctk.CTkLabel(
            self.codigoframe,
            text="Código",
            font=("Arial", 16, "bold")
        )
        self.lcodigo.pack(pady=10)

        # SECCIÓN 2: CANTIDAD
        self.cantidadframe = ctk.CTkScrollableFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.cantidadframe.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.lcantidad = ctk.CTkLabel(
            self.cantidadframe,
            text="Cantidad",
            font=("Arial", 16, "bold")
        )
        self.lcantidad.pack(pady=10)

        # SECCIÓN 3: DETALLES
        self.detallesframe = ctk.CTkScrollableFrame(self.frame_columnas, fg_color="#2B2B2B", corner_radius=8)
        self.detallesframe.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.ldetalles = ctk.CTkLabel(
            self.detallesframe,
            text="Detalles",
            font=("Arial", 16, "bold")
        )
        self.ldetalles.pack(pady=10)

        # ====================================================
        # 3. BLOQUE MEDIO (FORMULARIO DE CAPTURA)
        # ====================================================
        self.frame_medio_inner = ctk.CTkFrame(self.medio, fg_color="transparent")
        self.frame_medio_inner.pack(fill="both", expand=True, padx=10, pady=10)

        # Campo 1: Proveedor
        self.f_prov = ctk.CTkFrame(self.frame_medio_inner, fg_color="transparent")
        self.f_prov.pack(side="left", padx=5)
        self.blprovedor = ctk.CTkLabel(self.f_prov, text="ID / Proveedor:", font=("Arial", 11, "bold"))
        self.blprovedor.pack(anchor="w")
        self.blprovedorbox = ctk.CTkEntry(self.f_prov, width=150)
        self.blprovedorbox.pack(pady=(2, 0))

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
        self.blcantidadbox = ctk.CTkEntry(self.f_cant, width=120)
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

        # --- F1 ---
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

        self.lf1 = ctk.CTkLabel(self.item_f1, text="Buscar Proveedor", font=("Arial", 12, "bold"))
        self.lf1.pack(side="left")

        # --- F2 ---
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
        self.blprovedorbox.bind("<Return>", lambda e: self.blcodigobox.focus())
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
        """Abre el modal de búsqueda de proveedores (F1)"""
        def al_elegir(prov):
            self.blprovedorbox.delete(0, 'end')
            self.blprovedorbox.insert(0, str(prov.get('id', '')))
            self.nombre_proveedor = prov.get('nombre', '')

        VentanaBusquedaProveedor(self, al_seleccionar_callback=al_elegir)

    def busquedacodigo(self):
        """Verifica que haya proveedor antes de abrir el modal de productos (F2)"""
        id_prov = self.blprovedorbox.get().strip()
        if not id_prov:
            messagebox.showwarning(
                "Proveedor requerido",
                "Primero seleccione un proveedor (F1) antes de buscar productos."
            )
            return

        def al_elegir(codigo):
            self.blcodigobox.delete(0, 'end')
            self.blcodigobox.insert(0, codigo)
            self.enter()  # Carga automáticamente los detalles al seleccionar

        VentanaBusqueda(
            self,
            al_seleccionar_callback=al_elegir,
            modo="faltantes",
            id_proveedor=id_prov
        )

    def cancelar(self):
        """Limpia todas las cajas del formulario"""
        self.nombre_proveedor = ""
        self.blprovedorbox.delete(0, 'end')
        self.blcodigobox.delete(0, 'end')
        self.blcantidadbox.delete(0, 'end')
        self.bldetallesbox.configure(state="normal")
        self.bldetallesbox.delete(0, 'end')
        self.bldetallesbox.configure(state="disabled")

    def borrarproducto(self):
        """Limpia solo la casilla de producto, cantidad y detalles (F3)"""
        self.blcodigobox.delete(0, 'end')
        self.blcantidadbox.delete(0, 'end')
        self.bldetallesbox.configure(state="normal")
        self.bldetallesbox.delete(0, 'end')
        self.bldetallesbox.configure(state="disabled")
        
    def renderizar_tabla(self):
            """Limpia los widgets visuales de las 3 columnas y los vuelve a dibujar desde self.lista_productos"""
            columnas = [self.codigoframe, self.cantidadframe, self.detallesframe]
    
            for frame in columnas:
                widgets = frame.winfo_children()
                for w in widgets[1:]:
                    w.destroy()
    
            for p in self.lista_productos:
                ctk.CTkLabel(self.codigoframe, text=p["codigo"], font=("Arial", 12)).pack(pady=2)
                ctk.CTkLabel(self.cantidadframe, text=str(p["cantidad"]), font=("Arial", 12)).pack(pady=2)
                ctk.CTkLabel(self.detallesframe, text=p["detalles"], font=("Arial", 12)).pack(pady=2)
    

    def subir(self):
        """Agrega un producto validado a la lista en memoria y actualiza la tabla"""
        codigo = self.blcodigobox.get().strip()
        detalles = self.bldetallesbox.get().strip()

        try:
            cantidad = int(self.blcantidadbox.get().strip())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                return
        except ValueError:
            cantidad = 1

        if not codigo or not detalles:
            messagebox.showwarning("Advertencia", "Primero presione Enter para cargar los datos del producto.")
            return

        for item in self.lista_productos:
            if item["codigo"] == codigo:
                item["cantidad"] += cantidad
                self.renderizar_tabla()
                self.borrarproducto()  # Conserva el proveedor seleccionado
                return

        self.lista_productos.append({
            "codigo": codigo,
            "cantidad": cantidad,
            "detalles": detalles
        })

        self.renderizar_tabla()
        self.borrarproducto()  # Conserva el proveedor seleccionado

    def enter(self, event=None):
        id_prov = self.blprovedorbox.get().strip()
        if not id_prov:
            messagebox.showwarning("Proveedor requerido", "Primero seleccione un proveedor.")
            return

        codigo = self.blcodigobox.get().strip()
        if not codigo:
            return

        try:
            cantidad = int(self.blcantidadbox.get().strip())
            if cantidad <= 0:
                messagebox.showerror("Error", "No se permiten cantidades negativas.")
                return
        except ValueError:
            cantidad = 1
            self.blcantidadbox.delete(0, END)
            self.blcantidadbox.insert(0, str(cantidad))

        producto = obtener_producto_de_proveedor(codigo, id_prov)
        if not producto:
            messagebox.showerror(
                "No válido",
                "El producto no existe o no pertenece al proveedor seleccionado."
            )
            return

        nombre = producto.get('nombre') or ''
        descripcion = producto.get('descripcion') or ''
        texto_detalles = f"{nombre} - {descripcion}" if descripcion else nombre

        self.bldetallesbox.configure(state="normal")
        self.bldetallesbox.delete(0, END)
        self.bldetallesbox.insert(0, texto_detalles)
        self.bldetallesbox.configure(state="disabled")
    
    def subirsistema(self):
        """Genera/actualiza el archivo .txt de faltantes del proveedor y limpia la tabla (F4)"""
        id_prov = self.blprovedorbox.get().strip()
        if not id_prov:
            messagebox.showwarning("Proveedor requerido", "Seleccione un proveedor antes de subir la lista.")
            return

        if not self.lista_productos:
            messagebox.showwarning("Lista vacía", "Agregue al menos un producto a la tabla antes de subir.")
            return

        # Obtener el nombre del proveedor (desde F1 o consultando por ID en MySQL)
        nombre_prov = self.nombre_proveedor or obtener_nombre_proveedor(id_prov)
        if not nombre_prov:
            messagebox.showerror("Error", "El ID del proveedor no existe en la base de datos.")
            return

        try:
            # Genera o acumula en Faltantes/Faltantes_<nombre_prov>.txt y lo abre
            listafaltantes(nombre_prov, self.lista_productos)

            # Limpiar tabla en memoria, vista y formulario para el siguiente pedido
            self.lista_productos.clear()
            self.renderizar_tabla()
            self.cancelar()

            messagebox.showinfo("Éxito", f"Lista de faltantes guardada para {nombre_prov}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el archivo de faltantes: {e}")

    def cargar_desde_txt(self, ruta_archivo):
        """Lee un archivo .txt de faltantes, asigna el proveedor y despliega los productos en la tabla"""
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

                    # Omitir encabezados de columna
                    if texto.lower().startswith(("código", "codigo")) and ("cantidad" in texto.lower() or "detalles" in texto.lower()):
                        continue

                    # Parsear líneas separadas por '|' o tabulador
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
                                "detalles": det
                            })
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la lista de faltantes: {e}")
            return

        if not nombre_prov:
            nombre_prov = os.path.basename(ruta_archivo).replace("Faltantes_", "").replace(".txt", "")

        # Buscar el ID del proveedor en MySQL para rellenar el campo ID / Proveedor
        datos_prov = buscarprovedor(nombre_prov)
        self.blprovedorbox.delete(0, END)
        if datos_prov:
            self.blprovedorbox.insert(0, str(datos_prov["id"]))
            self.nombre_proveedor = datos_prov["nombre"]
        else:
            self.nombre_proveedor = nombre_prov

        self.lista_productos = productos_cargados
        self.renderizar_tabla()