import customtkinter as ctk
from tkinter import messagebox, END
from Busquda import VentanaBusqueda
from Conexion import buscar_producto_por_codigo, guardarpromocion

class promociones(ctk.CTkFrame):
    def __init__(self, parent):
        super(). __init__(parent)

        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=10)

        self.izquierda = ctk.CTkFrame(self.contenedor)
        self.izquierda.pack(side="top", fill="both", expand=True, pady=(0, 10))

        self.derecha = ctk.CTkFrame(self.contenedor, height=90)
        self.derecha.pack(side="top", fill="x", pady=(10, 0))

        self.nuevos=ctk.CTkLabel(
            self.izquierda,
            text="Agregar una nueva promocion",
            font=("Arial", 18, "bold")
        )
        self.nuevos.pack(pady=5)

        self.nombre=ctk.CTkLabel(
            self.izquierda,
            text="nombre de la promocion",
            font=("Arial", 18, "bold")
        )
        self.nuevos.pack(pady=5)
        self.nombrebox=ctk.CTkEntry(self.izquierda, width=200)

        self.fproducto=ctk.CTkLabel(
            self.izquierda,
            text="Primer producto",
            font=("Arial", 12, "bold")
        )
        self.fproducto.pack(pady=5)
        self.fproductobox=ctk.CTkEntry(self.izquierda, width=200)
        self.fproductobox.pack(pady=5)
        self.fproducto.configure(state="disabled")
        self.fcantidad=ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.fcantidad.pack(pady=5)
        self.fcantidadbox=ctk.CTkEntry(self.izquierda, width=200)
        self.fcantidadbox.pack(pady=5)
        self.fcantidad.configure(state="disabled")

        self.sproducto=ctk.CTkLabel(
            self.izquierda,
            text="Segundo producto",
            font=("Arial", 12, "bold")
        )
        self.sproducto.pack(pady=5)
        self.sproductobox=ctk.CTkEntry(self.izquierda, width=200)
        self.sproductobox.pack(pady=5)
        self.sproductobox.configure(state="disabled")
        self.scantidad=ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.scantidad.pack(pady=5)
        self.scantidadbox=ctk.CTkEntry(self.izquierda, width=200)
        self.scantidadbox.pack(pady=5)
        self.scantidadbox.configure(state="disabled")


        self.tproducto=ctk.CTkLabel(
            self.izquierda,
            text="Tercer producto",
            font=("Arial", 12, "bold")
        )
        self.tproducto.pack(pady=5)
        self.tproductobox=ctk.CTkEntry(self.izquierda, width=200)
        self.tproductobox.pack(pady=5)
        self.tproductobox.configure(state="disabled")
        self.tcantidad=ctk.CTkLabel(
            self.izquierda,
            text="Cantidad",
            font=("Arial", 12, "bold")
        )
        self.tcantidad.pack(pady=5)
        self.tcantidadbox=ctk.CTkEntry(self.izquierda, width=200)
        self.tcantidadbox.pack(pady=5)
        self.tcantidadbox.configure(state="disabled")

        self.precio=ctk.CTkLabel(
            self.izquierda,
            text="Precio",
            font=("Arial", 12, "bold")
        )
        self.precio.pack(pady=5)
        self.preciobox=ctk.CTkEntry(self.izquierda, width=200)
        self.preciobox.pack(pady=5)

        self.btnbuscar=ctk.CTkButton(
            self.izquierda,
            text="Buscar Producto",
            fg_color="#2535C9",
            hover_color="#170B59", 
            text_color="#FFFFFF",
            width=200,
            command= self.buscar
        )
        self.btnbuscar.pack(pady=5)

        self.btnguardar=ctk.CTkButton(
            self.izquierda,
            text="Guardar",
            fg_color="#25C935",
            hover_color="#0B591B", 
            text_color="#FFFFFF",
            width=200,
            command= self.guardar
        )
        self.btnguardar.pack(pady=5)

        self.btncancelar=ctk.CTkButton(
            self.izquierda,
            text="Cancelar",
            fg_color="#EF4444",
            hover_color="#6B1818", 
            text_color="#FFFFFF",
            width=200,
            command= self.cancelar
        )
        self.btncancelar.pack(pady=5)

    def cancelar(self):
        self.fproducto.delete(0, END)
        self.fcantidad.delete(0, END)

        self.sproducto.configure(state="normal")
        self.sproducto.delete(0, END)
        self.sproducto.configure(state="disabled")
        self.scantidad.configure(state="normal")
        self.scantidad.delete(0, END)
        self.scantidad.configure(state="disabled")

        self.tproducto.configure(state="normal")
        self.tproducto.delete(0, END)
        self.tproducto.configure(state="disabled")
        self.tcantidad.configure(state="normal")
        self.tcantidad.delete(0, END)
 
        self.tcantidad.configure(state="disabled")

    def guardar(self):
        pass
    def buscar(self):
        """Asigna secuencialmente hasta 3 productos y desbloquea su campo de cantidad"""
        if self.tproductobox.get().strip():
            messagebox.showinfo("Límite alcanzado", "Ya seleccionaste los 3 productos permitidos para la promoción.")
            return

        def al_elegir(codigo):
            prod = buscar_producto_por_codigo(codigo)
            texto_mostrar = f"{codigo} - {prod['nombre']}" if prod else str(codigo)
            self.codigos_promo.append(codigo)

            # 1er producto vacío -> llena fproductobox y desbloquea fcantidadbox
            if not self.fproductobox.get().strip():
                self.fproductobox.configure(state="normal")
                self.fproductobox.delete(0, END)
                self.fproductobox.insert(0, texto_mostrar)
                self.fproductobox.configure(state="disabled")

                self.fcantidadbox.configure(state="normal")
                self.fcantidadbox.focus()

            # 2do producto vacío -> llena sproductobox y desbloquea scantidadbox
            elif not self.sproductobox.get().strip():
                self.sproductobox.configure(state="normal")
                self.sproductobox.delete(0, END)
                self.sproductobox.insert(0, texto_mostrar)
                self.sproductobox.configure(state="disabled")

                self.scantidadbox.configure(state="normal")
                self.scantidadbox.focus()

            # 3er producto vacío -> llena tproductobox, desbloquea tcantidadbox y bloquea Buscar
            elif not self.tproductobox.get().strip():
                self.tproductobox.configure(state="normal")
                self.tproductobox.delete(0, END)
                self.tproductobox.insert(0, texto_mostrar)
                self.tproductobox.configure(state="disabled")

                self.tcantidadbox.configure(state="normal")
                self.tcantidadbox.focus()
                self.btnbuscar.configure(state="disabled")

        VentanaBusqueda(self, al_seleccionar_callback=al_elegir, modo="ventas")