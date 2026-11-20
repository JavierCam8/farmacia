import os
import smtplib
from email.message import EmailMessage


def enviar_correo(destinatario, asunto, cuerpo, ruta_adjunto=None):
    remitente = "correopuebas1@gmail.com"
    password_app = "Prueba.123"  # Tu clave de aplicación de 16 letras

    if "tu_correo" in remitente or "xxxx" in password_app:
        return False, "Configura primero tu correo real y contraseña de aplicación en enviarcorreo.py."

    # Quitar espacios de la contraseña de aplicación para evitar errores de lectura
    password_limpia = password_app.replace(" ", "").strip()

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
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(remitente, password_limpia)
            smtp.send_message(msg)
        return True, "Correo enviado correctamente."

    except smtplib.SMTPAuthenticationError:
        return False, "Correo o contraseña de aplicación incorrectos. Verifica tu clave de 16 letras."
    except smtplib.SMTPServerDisconnected:
        return False, "El servidor o tu antivirus/red cerró la conexión. Prueba desactivando temporalmente el escudo de correo o cambiando de Wi-Fi."
    except Exception as e:
        return False, f"No se pudo enviar el correo: {e}"