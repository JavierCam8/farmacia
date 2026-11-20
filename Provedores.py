import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, END
from Busquda import VentanaBusqueda, VentanaBusquedaProveedor
from enviarcorreo import enviar_correo
from Conexion import guardarprovedor, guardarproducto, buscarprovedor, obtener_proveedores, actualizarprovedor, obtener_productos, buscarproducto_nombre, actualizarproducto, buscar_producto_por_codigo

class FrameProvedor(ctk.CTkFrame):
    def __init__(self, parent):
        super(). __init__(parent)

        self.titulo=ctk.CTkLabel(
            self,
            text="Provedores",
            font=("Arial", 22, "bold"),
        )
        self.titulo.pack(pady=(15, 10))

        self.contenedor=ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        self.actualizarprovedor=ctk.CTkFrame(self.contenedor)
        self.actualizarprovedor.pack(side="left", fill="both", expand=True, padx=(0,5))

        self.productos=ctk.CTkScrollableFrame(self.contenedor, scrollbar_button_color="#2456D4", scrollbar_button_hover_color="#0F0DAA")
        self.productos.pack(side="left", fill="both", expand=True, padx=5)

        self.pedidos=ctk.CTkFrame(self.contenedor)
        self.pedidos.pack(side="left", fill="both", expand=True, padx=(5,0))

################################## primera parte cambiar y guardar
        self.btitulo=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Actualizar informacion",
            font=("Arial", 12, "bold"),
        )
        self.btitulo.pack(pady=5)

        self.bpnombre=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Nombre del provedeor",
            font=("Arial", 12, "bold")
        )
        self.bpnombre.pack(pady=3)
        self.bpnombrebox=ctk.CTkComboBox(self.actualizarprovedor,  values=[""], width=300, command=self.cargar_datos_proveedor)
        self.bpnombrebox.pack(pady=3)

        self.cnombre=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Nombre:",
            font=("Arial", 12, "bold")
        )
        self.cnombre.pack(pady=2)
        self.cnombrebox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.cnombrebox.pack(pady=2)

        self.ctelefono=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Telefono",
            font=("Arial", 12, "bold")
        )
        self.ctelefono.pack(pady=2)
        self.ctelefonobox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.ctelefonobox.pack(pady=2)

        self.crfc=ctk.CTkLabel(
            self.actualizarprovedor,
            text="RFC",
            font=("Arial", 12, "bold")
        )
        self.crfc.pack(pady=2)
        self.crfcbox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.crfcbox.pack(pady=2)

        self.cemail=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Email",
            font=("Arial", 12, "bold")
        )
        self.cemail.pack(pady=2)
        self.cemailbox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.cemailbox.pack(pady=2)

        self.cdireccion=ctk.CTkLabel(
            self.actualizarprovedor,
            text="Direccion",
            font=("Arial", 12, "bold")
        )
        self.cdireccion.pack(pady=2)
        self.cdireccionbox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.cdireccionbox.pack(pady=2)

        self.cestado=ctk.CTkLabel(
            self.actualizarprovedor, 
            text="Estado",
            font=("Arial", 12, "bold")
        )
        self.cestado.pack(pady=2)
        self.cestadobox=ctk.CTkEntry(self.actualizarprovedor, width=300)
        self.cestadobox.pack(pady=2)

        self.btnbuscar=ctk.CTkButton(
            self.actualizarprovedor,
            text="Buscarprovedor",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            width=300,
            command=self.abrir_busqueda_proveedor
        )
        self.btnbuscar.pack(pady=2)

        self.btcambiar=ctk.CTkButton(
            self.actualizarprovedor,
            text="Cambiar datos",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            width=300,
            command=self.cambiar
        )
        self.btcambiar.pack(pady=2)
        self.btcambiar.configure(state="disabled")

        self.btguardar=ctk.CTkButton(
            self.actualizarprovedor,
            text="Guardar",
            fg_color="#10B981",
            hover_color="#09650F",
            text_color="#FFFFFE",
            width=300,
            command=self.guardarprovedor
        )
        self.btguardar.pack(pady=3)

        self.btcancelarcambio=ctk.CTkButton(
            self.actualizarprovedor,
            text="Cancelar",
            fg_color="#de1323",
            hover_color="#690e15",
            text_color="#FFFFFF",
            width=300,
            command=self.cancelarcambio
        )
        self.btcancelarcambio.pack(pady=2)

################################ parte dos productos

        self.productostitulo=ctk.CTkLabel(
            self.productos,
            text="Productos",
            font=("Arial", 18, "bold")
        )
        self.productostitulo.pack(pady=5)

        self.bproducto=ctk.CTkLabel(
            self.productos,
            text="Nombre del producto",
            font=("Arial", 12, "bold")
        )
        self.bproducto.pack(pady=2)
        self.buscarproducto=ctk.CTkComboBox(self.productos, values=[""], width=300, command=self.buscar_producto)
        self.buscarproducto.pack(pady=2)

        self.nombreproducto=ctk.CTkLabel(
            self.productos,
            text="Nombre del producto",
            font=("Arial", 12, "bold")
        )
        self.nombreproducto.pack(pady=2)
        self.nombreproductobox=ctk.CTkEntry(self.productos, width=300)
        self.nombreproductobox.pack(pady=2)
        
        self.marca=ctk.CTkLabel(
            self.productos,
            text="Marca del producto",
            font=("Arial", 12, "bold")
        )
        self.marca.pack(pady=2)
        self.marcabox=ctk.CTkEntry(self.productos, width=300)
        self.marcabox.pack(pady=2)

        self.codigobarras=ctk.CTkLabel(
            self.productos,
            text="codigo de barras del producto",
            font=("Arial", 12, "bold")
        )
        self.codigobarras.pack(pady=2)
        self.codigobarrasbox=ctk.CTkEntry(self.productos, width=300)
        self.codigobarrasbox.pack(pady=2)

        self.codigo=ctk.CTkLabel(
            self.productos,
            text="codigo del producto",
            font=("Arial", 12, "bold")
        )
        self.codigo.pack(pady=2)
        self.codigobox=ctk.CTkEntry(self.productos, width=300)
        self.codigobox.pack(pady=2)

        self.descripcion=ctk.CTkLabel(
            self.productos,
            text="Descripcion del producto",
            font=("Arial", 12, "bold")
        )
        self.descripcion.pack(pady=2)
        self.descripcionbox=ctk.CTkEntry(self.productos, width=300)
        self.descripcionbox.pack(pady=2)

        self.requisito=ctk.CTkLabel(
            self.productos,
            text="Receta o Identificación para comprar el producto",
            font=("Arial", 12, "bold")
        )
        self.requisito.pack(pady=2)
        self.requisitobox=ctk.CTkComboBox(self.productos, width=300, values=["Receta", "Identificación","Ninguno"])
        self.requisitobox.pack(pady=2)

        self.categoria=ctk.CTkLabel(
            self.productos,
            text="Categoria del producto",
            font=("Arial", 12, "bold")
        )
        self.categoria.pack(pady=2)
        self.categoriabox=ctk.CTkComboBox(self.productos, values=["Limitado", "Sin limitaciones"], width=300)
        self.categoriabox.pack(pady=2)

        self.costo=ctk.CTkLabel(
            self.productos,
            text="Costo del producto",
            font=("Arial", 12, "bold")
        )
        self.costo.pack(pady=2)
        self.costobox=ctk.CTkEntry(self.productos, width=300)
        self.costobox.pack(pady=2)

        self.provedor=ctk.CTkLabel(
            self.productos,
            text="Provedor del producto",
            font=("Arial", 12, "bold")
        )
        self.provedor.pack(pady=2)
        self.provedorbox=ctk.CTkComboBox(self.productos, values=[""], width=300)
        self.provedorbox.pack(pady=2)

        self.venta=ctk.CTkLabel(
            self.productos,
            text="Precio de venta del producto",
            font=("Arial", 12, "bold")
        )
        self.venta.pack(pady=2)
        self.ventabox=ctk.CTkEntry(self.productos, width=300)
        self.ventabox.pack(pady=2)

        self.btnbuscarproducto = ctk.CTkButton(
            self.productos,
            text="Buscar producto",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            width=300,
            command=self.abrir_busqueda_producto
        )
        self.btnbuscarproducto.pack(pady=2)

        self.btcambiarproducto=ctk.CTkButton(
            self.productos,
            text="Cambiar informacion",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            width=300,
            command=self.cambioproducto
        )
        self.btcambiarproducto.pack(pady=2)
        self.btcambiarproducto.configure(state="disabled")

        self.btpguardar=ctk.CTkButton(
            self.productos,
            text="Guardar",
            fg_color="#10B981",
            hover_color="#059669",
            text_color="#FFFFFF",
            width=300,
            command=self.guardarproducto
        )
        self.btpguardar.pack(pady=2)

        self.btcancelar=ctk.CTkButton(
            self.productos,
            text="Cancelar",
            fg_color="#EB2525",
            hover_color="#951515",
            text_color="#FFFFFF",
            width=300,
            command=self.cancelar
        )
        self.btcancelar.pack(pady=2)

##################################### tercer parte pedidos

        self.titulopedidos=ctk.CTkLabel(
            self.pedidos,
            text="Pedidos",
            font=("Arial", 18, "bold")
        )
        self.titulopedidos.pack(pady=2)

        self.lbproductos=ctk.CTkLabel(
            self.pedidos,
            text="Lista de pedidos", 
            font=("Arial", 12, "bold")
        )
        self.lbproductos.pack(pady=3)

        self.pedidoscombo= ctk.CTkComboBox(
            self.pedidos,
            values=[""],
            height=50,
            width=300,
            command=self.obtenerfaltantes
        )
        self.pedidoscombo.pack(pady=5)

        self.provedorfaltante = ctk.CTkLabel(
            self.pedidos,
            text="Proveedor designado", 
            font=("Arial", 12, "bold")
        )
        self.provedorfaltante.pack(pady=3)
        self.provedorfaltantebox = ctk.CTkEntry(self.pedidos, width=250)
        self.provedorfaltantebox.pack(pady=3)
        self.provedorfaltantebox.configure(state="disabled")

        self.btactualizarlista = ctk.CTkButton(
            self.pedidos,
            text="Actualizar lista",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            command=self.cargar_faltantes
        )
        self.btactualizarlista.pack(pady=5)

        self.btaenviar=ctk.CTkButton(
            self.pedidos,
            text="Enviar",
            fg_color="#3AB91D",
            hover_color="#2D7E10",
            text_color="#FFFFFF",
            command=self.enviar
        )
        self.btaenviar.pack(pady=5)

        self.btborrar=ctk.CTkButton(
            self.pedidos,
            text="Borrar",
            fg_color="#B91D1D",
            hover_color="#A91D1D",
            text_color="#FFFFFF",
            command=self.borrar
        )
        self.btborrar.pack(pady=5)

        self.btcancelar=ctk.CTkButton(
            self.pedidos,
            text="Cancelar",
            fg_color="#B91D1D",
            hover_color="#A91D1D",
            text_color="#FFFFFF",
            command=self.cancelarpedido
        )
        self.btcancelar.pack(pady=5)

        self.proveedor_actual_id = None
        self.cargar_proveedores()

        self.producto_actual_id = None
        self.cargar_productos()

        self.cargar_faltantes()

    def obtenerfaltantes(self):
        pass

    def cargar_productos(self):
        productos = obtener_productos()
        nombres = [p["nombre"] for p in productos]

        if nombres:
            self.buscarproducto.configure(values=nombres)
        else:
            self.buscarproducto.configure(values=[""])
        self.buscarproducto.set("")

    def buscar_producto(self, _seleccion=None):
        nombre_producto = self.buscarproducto.get().strip()
        if not nombre_producto:
            messagebox.showinfo("Error", "No hay ningún producto seleccionado")
            return

        datos = buscarproducto_nombre(nombre_producto)
        if not datos:
            messagebox.showwarning("Sin resultados", "No se encontró el producto en la base de datos")
            return

        self.producto_actual_id = datos["id"]
        self.btcambiarproducto.configure(state="normal")

        # Rellenar Entry
        self.nombreproductobox.delete(0, END)
        self.nombreproductobox.insert(0, datos["nombre"] or "")

        self.marcabox.delete(0, END)
        self.marcabox.insert(0, datos["marca"] or "")

        self.codigobarrasbox.delete(0, END)
        self.codigobarrasbox.insert(0, datos["codigobarras"] or "")

        self.codigobox.delete(0, END)
        self.codigobox.insert(0, datos["codigo"] or "")

        self.descripcionbox.delete(0, END)
        self.descripcionbox.insert(0, datos["descripcion"] or "")

        self.costobox.delete(0, END)
        self.costobox.insert(0, str(datos["precio_costo"]) if datos["precio_costo"] is not None else "")

        self.ventabox.delete(0, END)
        self.ventabox.insert(0, str(datos["precio_venta"]) if datos["precio_venta"] is not None else "")

        # Rellenar ComboBox
        self.requisitobox.set(datos["requisito"] or "")
        self.categoriabox.set(datos["categoria"] or "")
        self.provedorbox.set(datos["nombre_proveedor"] or "")

    def cambioproducto(self):
        if not self.producto_actual_id:
            messagebox.showerror("Error", "Primero busque un producto para modificar")
            return

        nombre = self.nombreproductobox.get().strip()
        marca = self.marcabox.get().strip()
        codigobarras = self.codigobarrasbox.get().strip()
        codigo = self.codigobox.get().strip()
        descripcion = self.descripcionbox.get().strip()
        requisitos = self.requisitobox.get().strip()
        categoria = self.categoriabox.get().strip()
        costo = self.costobox.get().strip()
        provedor_nombre = self.provedorbox.get().strip()
        venta = self.ventabox.get().strip()

        if not all([nombre, marca, codigobarras, codigo, descripcion, requisitos, categoria, costo, provedor_nombre, venta]):
            messagebox.showerror("Error", "Llene todos los campos")
            return

        id_provedor = self.mapa_proveedores.get(provedor_nombre)
        if not id_provedor:
            messagebox.showerror("Error", "Seleccione un proveedor válido de la lista")
            return

        exito, mensaje = actualizarproducto(
            self.producto_actual_id,
            marca,
            nombre,
            codigobarras,
            codigo,
            descripcion,
            costo,
            venta,
            id_provedor,
            requisitos,
            categoria,
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def guardarproducto(self):
        nombre = self.nombreproductobox.get().strip()
        marca = self.marcabox.get().strip()
        codigobarras = self.codigobarrasbox.get().strip()
        codigo = self.codigobox.get().strip()
        descripcion = self.descripcionbox.get().strip()
        requisitos = self.requisitobox.get().strip()
        categoria = self.categoriabox.get().strip()
        costo = self.costobox.get().strip()
        provedor_nombre = self.provedorbox.get().strip()
        venta = self.ventabox.get().strip()

        if not all([nombre, marca, codigobarras, codigo, descripcion, requisitos, categoria, costo, provedor_nombre, venta]):
            messagebox.showerror("Error", "Llene todos los campos")
            return

        id_provedor = self.mapa_proveedores.get(provedor_nombre)
        if not id_provedor:
            messagebox.showerror("Error", "Seleccione un proveedor válido de la lista")
            return

        exito, mensaje = guardarproducto(
            marca, nombre, codigobarras, codigo, descripcion, costo, venta, id_provedor, requisitos, categoria
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelar()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def cambiar(self):
        if not self.proveedor_actual_id:
            messagebox.showerror("Error", "Primero busque un proveedor para modificar")
            return

        nombre = self.cnombrebox.get().strip()
        telefono = self.ctelefonobox.get().strip()
        rfc = self.crfcbox.get().strip()
        email = self.cemailbox.get().strip()
        direccion = self.cdireccionbox.get().strip()
        estado = self.cestadobox.get().strip()

        if not all([nombre, telefono, rfc, email, direccion, estado]):
            messagebox.showerror("Error", "Datos incompletos")
            return

        exito, mensaje = actualizarprovedor(
            self.proveedor_actual_id, nombre, telefono, rfc, email, direccion, estado
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelarcambio()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)

    def cancelarcambio(self):
        self.proveedor_actual_id = None
        self.bpnombrebox.set("")
        self.cnombrebox.delete(0, END)
        self.ctelefonobox.delete(0, END)
        self.crfcbox.delete(0, END)
        self.cemailbox.delete(0, END)
        self.cdireccionbox.delete(0, END)
        self.cestadobox.delete(0, END)
        self.btcambiar.configure(state="disabled")    

    def guardarprovedor(self):
        nombre = self.cnombrebox.get().strip()
        telefono = self.ctelefonobox.get().strip()
        rfc = self.crfcbox.get().strip()
        email = self.cemailbox.get().strip()
        direccion = self.cdireccionbox.get().strip()
        estado = self.cestadobox.get().strip()

        if not all([nombre, telefono, rfc, email, direccion, estado]):
            messagebox.showerror("Error", "Datos incompletos")
            return

        exito, mensaje = guardarprovedor(nombre, telefono, rfc, email, direccion, estado)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.cancelarcambio()
            self.cargar_proveedores()
        else:
            messagebox.showerror("Error", mensaje)

    def cancelar(self):
        self.producto_actual_id = None
        self.buscarproducto.set("")
        self.nombreproductobox.delete(0, END)
        self.marcabox.delete(0, END)
        self.codigobarrasbox.delete(0, END)
        self.codigobox.delete(0, END)
        self.descripcionbox.delete(0, END)
        self.requisitobox.set("")
        self.categoriabox.set("")
        self.costobox.delete(0, END)
        self.provedorbox.set("")
        self.ventabox.delete(0, END)
        self.btcambiarproducto.configure(state="disabled")

    def cargar_proveedores(self):
        proveedores = obtener_proveedores()
        self.mapa_proveedores = {p["nombre"]: p["id"] for p in proveedores}
        nombres = list(self.mapa_proveedores.keys())

        if nombres:
            self.bpnombrebox.configure(values=nombres)
            self.provedorbox.configure(values=nombres)
        else:
            self.bpnombrebox.configure(values=[""])
            self.provedorbox.configure(values=[""])
        self.bpnombrebox.set("")
        self.provedorbox.set("")

    

    def buscarprovedor(self):
        provedor = self.bpnombrebox.get().strip()
        if not provedor:
            messagebox.showinfo("Error", "No hay ningún proveedor seleccionado")
            return

        datos = buscarprovedor(provedor)

        if not datos:
            messagebox.showwarning("Sin resultados", "No se encontró el proveedor en la base de datos")
            return

        self.proveedor_actual_id = datos["id"]
        self.btcambiar.configure(state="normal")

        self.cnombrebox.delete(0, END)
        self.cnombrebox.insert(0, datos["nombre"] or "")

        self.ctelefonobox.delete(0, END)
        self.ctelefonobox.insert(0, datos["telefono"] or "")

        self.crfcbox.delete(0, END)
        self.crfcbox.insert(0, datos["rfc"] or "")

        self.cemailbox.delete(0, END)
        self.cemailbox.insert(0, datos["email"] or "")

        self.cdireccionbox.delete(0, END)
        self.cdireccionbox.insert(0, datos["direccion"] or "")

        self.cestadobox.delete(0, END)
        self.cestadobox.insert(0, datos["estado"] or "")

    def enviar(self):
        """Obtiene el correo del proveedor desde MySQL y envía el archivo .txt adjunto"""
        archivo = self.pedidoscombo.get().strip()
        nombre_proveedor = self.provedorfaltantebox.get().strip()

        if not archivo or not nombre_proveedor:
            messagebox.showwarning("Sin selección", "Seleccione una lista de pedidos primero.")
            return

        ruta = os.path.join("Faltantes", archivo)
        if not os.path.exists(ruta):
            messagebox.showerror("Error", "El archivo de pedido ya no existe.")
            self.cargar_faltantes()
            return

        datos_prov = buscarprovedor(nombre_proveedor)
        if not datos_prov or not datos_prov.get("email"):
            messagebox.showerror(
                "Sin correo",
                f"El proveedor '{nombre_proveedor}' no tiene un correo registrado en la base de datos."
            )
            return

        correo_destino = datos_prov["email"]
        confirmar = messagebox.askyesno(
            "Confirmar envío",
            f"¿Enviar '{archivo}' al correo:\n{correo_destino}?"
        )
        if not confirmar:
            return

        exito, mensaje = enviar_correo(
            destinatario=correo_destino,
            asunto=f"Pedido de productos faltantes - {nombre_proveedor}",
            cuerpo=f"Estimado(a) {nombre_proveedor},\n\nAdjunto la lista de productos requeridos.\n\nSaludos.",
            ruta_adjunto=ruta,
        )

        if exito:
            messagebox.showinfo("Correo enviado", mensaje)
            if messagebox.askyesno("Eliminar archivo", "¿Desea borrar el archivo .txt ya enviado?"):
                os.remove(ruta)
            self.cancelarpedido()
            self.cargar_faltantes()
        else:
            messagebox.showerror("Error al enviar", mensaje)
    def borrar(self):
        """Elimina definitivamente el archivo .txt seleccionado"""
        archivo = self.pedidoscombo.get().strip()
        if not archivo:
            messagebox.showwarning("Sin selección", "Seleccione un pedido de la lista para borrar.")
            return

        ruta = os.path.join("Faltantes", archivo)
        if not messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente '{archivo}'?"):
            return

        try:
            if os.path.exists(ruta):
                os.remove(ruta)
            messagebox.showinfo("Eliminado", "Lista de faltantes eliminada.")
            self.cancelarpedido()
            self.cargar_faltantes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el archivo: {e}")
            
    def cancelarpedido(self):
        """Limpia la selección actual sin borrar el archivo"""
        self.pedidoscombo.set("")
        self.limpiar_proveedor_designado()

    def cargar_faltantes(self):
        """Carga en pedidoscombo los archivos .txt de la carpeta Faltantes"""
        carpeta = "Faltantes"
        if not os.path.exists(carpeta):
            self.pedidoscombo.configure(values=[""])
            self.pedidoscombo.set("")
            return

        archivos = [f for f in os.listdir(carpeta) if f.endswith(".txt")]
        if archivos:
            self.pedidoscombo.configure(values=archivos)
        else:
            self.pedidoscombo.configure(values=[""])
        self.pedidoscombo.set("")

    def obtenerfaltantes(self, _seleccion=None):
        """Lee el .txt elegido y muestra el proveedor designado en provedorfaltantebox"""
        archivo = self.pedidoscombo.get().strip()
        if not archivo:
            self.limpiar_proveedor_designado()
            return

        ruta = os.path.join("Faltantes", archivo)
        if not os.path.exists(ruta):
            messagebox.showerror("Error", "El archivo seleccionado ya no existe.")
            self.cargar_faltantes()
            return

        nombre_proveedor = ""
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.startswith("Proveedor:"):
                        nombre_proveedor = linea.replace("Proveedor:", "").strip()
                        break
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            return

        if not nombre_proveedor:
            nombre_proveedor = archivo.replace("Faltantes_", "").replace(".txt", "")

        self.provedorfaltantebox.configure(state="normal")
        self.provedorfaltantebox.delete(0, END)
        self.provedorfaltantebox.insert(0, nombre_proveedor)
        self.provedorfaltantebox.configure(state="disabled")

    def limpiar_proveedor_designado(self):
        self.provedorfaltantebox.configure(state="normal")
        self.provedorfaltantebox.delete(0, END)
        self.provedorfaltantebox.configure(state="disabled")

    def cargar_datos_proveedor(self, _seleccion=None):
        """Rellena los campos del proveedor al seleccionarlo en el ComboBox o desde el buscador"""
        provedor = self.bpnombrebox.get().strip()
        if not provedor:
            return

        datos = buscarprovedor(provedor)
        if not datos:
            messagebox.showwarning("Sin resultados", "No se encontró el proveedor en la base de datos")
            return

        self.proveedor_actual_id = datos["id"]
        self.btcambiar.configure(state="normal")

        self.cnombrebox.delete(0, END)
        self.cnombrebox.insert(0, datos["nombre"] or "")

        self.ctelefonobox.delete(0, END)
        self.ctelefonobox.insert(0, datos["telefono"] or "")

        self.crfcbox.delete(0, END)
        self.crfcbox.insert(0, datos["rfc"] or "")

        self.cemailbox.delete(0, END)
        self.cemailbox.insert(0, datos["email"] or "")

        self.cdireccionbox.delete(0, END)
        self.cdireccionbox.insert(0, datos["direccion"] or "")

        self.cestadobox.delete(0, END)
        self.cestadobox.insert(0, datos["estado"] or "")

    def abrir_busqueda_proveedor(self):
        """Abre el modal de búsqueda de proveedores y carga sus datos en el formulario"""
        def al_elegir(prov):
            nombre_prov = prov.get("nombre", "")
            if nombre_prov:
                self.bpnombrebox.set(nombre_prov)
                self.cargar_datos_proveedor(nombre_prov)

        VentanaBusquedaProveedor(self, al_seleccionar_callback=al_elegir)

    def abrir_busqueda_producto(self):
        """Abre el modal de búsqueda de productos y carga toda su información en el formulario"""
        def al_elegir(codigo):
            producto = buscar_producto_por_codigo(codigo)
            if not producto:
                messagebox.showwarning("Sin resultados", "No se encontró el producto seleccionado.")
                return

            nombre_prod = producto.get("nombre", "")
            if nombre_prod:
                self.buscarproducto.set(nombre_prod)
                self.buscar_producto(nombre_prod)

        VentanaBusqueda(self, al_seleccionar_callback=al_elegir, modo="ventas")
