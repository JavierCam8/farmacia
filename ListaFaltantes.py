import os
import re

def listafaltantes(nombre, lista_productos):
    carpeta = "Faltantes"
    os.makedirs(carpeta, exist_ok=True)

    # Limpiar caracteres no válidos para nombres de archivo en Windows
    nombre_limpio = re.sub(r'[\\/*?:"<>|]', "", str(nombre)).strip() or "General"
    ruta_archivo = os.path.join(carpeta, f"Faltantes_{nombre_limpio}.txt")

    # Diccionario para conservar el orden y acumular: {"nombre - detalles": cantidad}
    productos_acumulados = {}

    # 1. Si el archivo del proveedor ya existe, leer los productos que ya tenía
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as archivo_existente:
            for linea in archivo_existente:
                linea_limpia = linea.strip()
                # Ignorar líneas vacías, separadores y encabezados
                if (
                    not linea_limpia
                    or linea_limpia.startswith("=")
                    or linea_limpia.startswith("-")
                    or linea_limpia.startswith("Proveedor:")
                    or linea_limpia.startswith("CANT")
                ):
                    continue

                # Separar la primera columna (cantidad) del resto (nombre - detalles)
                partes = linea_limpia.split(None, 1)
                if len(partes) == 2 and partes[0].isdigit():
                    cant_guardada = int(partes[0])
                    desc_guardada = partes[1].strip()
                    productos_acumulados[desc_guardada] = (
                        productos_acumulados.get(desc_guardada, 0) + cant_guardada
                    )

    # 2. Agregar los nuevos productos (si ya existía el mismo producto, suma su cantidad)
    for p in lista_productos:
        cant_nueva = int(p.get("cantidad", 1))

        # Compatibilidad si guardas "detalles" ya combinado o "nombre" y "detalles" por separado
        if "nombre" in p and "detalles" in p and str(p["nombre"]) not in str(p["detalles"]):
            desc_nueva = f"{p['nombre']} - {p['detalles']}".strip()
        else:
            desc_nueva = str(p.get("detalles") or p.get("nombre", "")).strip()

        if desc_nueva:
            productos_acumulados[desc_nueva] = (
                productos_acumulados.get(desc_nueva, 0) + cant_nueva
            )

    # 3. Sobrescribir el archivo con los productos anteriores + los nuevos
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("==================================================\n")
        archivo.write(f"Proveedor: {nombre}\n")
        archivo.write("--------------------------------------------------\n")
        archivo.write("CANT     NOMBRE - DETALLES\n")
        archivo.write("--------------------------------------------------\n")

        for desc, cant in productos_acumulados.items():
            archivo.write(f"{str(cant).ljust(8)} {desc}\n")

        archivo.write("==================================================\n")

    os.startfile(ruta_archivo)