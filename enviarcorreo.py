import os
import smtplib
from email.message import EmailMessage


def enviar_correo(destinatario, asunto, cuerpo, ruta_adjunto=None):
    remitente = "tu_correo@gmail.com"
    password_app = "xxxx xxxx xxxx xxxx"  # Contraseña de aplicación de 16 letras

    msg = EmailMessage()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.set_content(cuerpo)

    if ruta_adjunto and os.path.exists(ruta_adjunto):
        with open(ruta_adjunto, "rb") as archivo:
            contenido = archivo.read()
        nombre_archivo = os.path.basename(ruta_adjunto)
        msg.add_attachment(
            contenido,
            maintype="text",
            subtype="plain",
            filename=nombre_archivo,
        )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, password_app)
            smtp.send_message(msg)
        return True, "Correo enviado correctamente."
    except Exception as e:
        return False, f"No se pudo enviar el correo: {e}"