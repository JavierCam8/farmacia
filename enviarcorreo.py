import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def enviar_correo(destinatario, asunto, cuerpo, ruta_adjunto=None):
    # Configuración
    sender_email = "@gmail.com"
    password = ""  # Contraseña de aplicación de Gmail (16 letras)
    smtp_server = "smtp.gmail.com"
    port = 587

    if "tu_correo" in sender_email or "xxxx" in password:
        return False, "Configura tu correo real y contraseña de aplicación en enviarcorreo.py."

    # Crear mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = destinatario
    message["Subject"] = asunto
    message.attach(MIMEText(cuerpo, "plain", "utf-8"))

    # Adjuntar el archivo .txt de faltantes si existe
    if ruta_adjunto and os.path.exists(ruta_adjunto):
        nombre_archivo = os.path.basename(ruta_adjunto)
        with open(ruta_adjunto, "rb") as archivo:
            parte = MIMEBase("application", "octet-stream")
            parte.set_payload(archivo.read())
        encoders.encode_base64(parte)
        parte.add_header(
            "Content-Disposition",
            f'attachment; filename="{nombre_archivo}"',
        )
        message.attach(parte)

    # Enviar correo
    try:
        password_limpia = password.replace(" ", "").strip()
        with smtplib.SMTP(smtp_server, port, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, password_limpia)
            server.sendmail(sender_email, destinatario, message.as_string())
        return True, "Correo enviado correctamente."
    except Exception as e:
        return False, f"No se pudo enviar el correo: {e}"