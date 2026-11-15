import customtkinter as ctk


class pagar(ctk.CTkToplevel):
    def __init__(self, parent, total_pagar="$0.00", callback=None):
        super().__init__(parent)
        self.geometry("260x240")
        self.title("Pagar")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.callback = callback

        self.lprecio = ctk.CTkLabel(
            self,
            text="Precio total:",
            font=("Arial", 14, "bold")
        )
        self.lprecio.pack(pady=(15, 3))
        self.lpreciobox = ctk.CTkEntry(self, width=180, justify="center")
        self.lpreciobox.insert(0, total_pagar)
        self.lpreciobox.configure(state="disabled")
        self.lpreciobox.pack(pady=3)

        self.tipopago = ctk.CTkLabel(
            self,
            text="Tipo de Pago:",
            font=("Arial", 14, "bold")
        )
        self.tipopago.pack(pady=(10, 3))
        self.combopago = ctk.CTkComboBox(
            self,
            values=["Efectivo", "Tarjeta de crédito", "Tarjeta de débito"],
            width=180
        )
        self.combopago.pack(pady=3)

        self.btnpagar = ctk.CTkButton(
            self,
            text="Pagar",
            fg_color="#1BCB21",
            hover_color="#0E781D",
            width=180,
            text_color="#000000",
            font=("Arial", 12, "bold"),
            command=self.pagar
        )
        self.btnpagar.pack(pady=(15, 5))

        self.btncancelar = ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#D80F0F",
            hover_color="#940F0F",
            text_color="#FFFFFF",
            width=180,
            font=("Arial", 12, "bold"),
            command=self.cancelar
        )
        self.btncancelar.pack(pady=4)

    def pagar(self):
        self.destroy()
        if self.callback:
            self.callback()

    def cancelar(self):
        self.destroy()