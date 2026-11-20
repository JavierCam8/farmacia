import mysql.connector
from mysql.connector import Error
import bcrypt
from tkinter import messagebox

def obtener_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='farmacia',
        port='3306'
    )

def validar(username, password):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_usuario = "SELECT * FROM usuarios WHERE username = %s"
        cursor.execute(sql_usuario, (username,))
        usuario = cursor.fetchone()

        if usuario:
            hash_almacenado = usuario["password"]
            # 1. Si está encriptada con bcrypt
            if hash_almacenado.startswith(("$2a$", "$2b$", "$2y$")):
                if bcrypt.checkpw(password.encode('utf-8'), hash_almacenado.encode('utf-8')):
                    return usuario

            # 2. Si está en texto plano (ej: "123456")
            elif hash_almacenado == password:
                sal = bcrypt.gensalt()
                nuevo_hash = bcrypt.hashpw(password.encode('utf-8'), sal).decode('utf-8')
                cursor.execute(
                    "UPDATE usuarios SET password = %s WHERE userid = %s",
                    (nuevo_hash, usuario["userid"])
                )
                conexion.commit()
                return usuario
        return None

    except Exception as err:
        messagebox.showerror("Error", f"BD: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def guardar(username, nombre, telefono, rfc, direccion, estado, email, password, rango):
    """Registra un nuevo trabajador encriptando la contraseña antes de guardar"""
    if not all([username, nombre, telefono, rfc, direccion, estado, email, password, rango]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT userid FROM usuarios WHERE username = %s"
        cursor.execute(sql_verificar, (username,))
        if cursor.fetchone():
            return False, "El nombre de usuario ya está registrado."

        sal = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), sal).decode('utf-8')

        sql_insert = """
            INSERT INTO usuarios (username, nombre, telefono, rfc, direccion, estado, email, password, rango)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (username, nombre, telefono, rfc, direccion, estado, email, password_hash, rango)

        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Usuario registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def obtener_trabajadores():
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT userid, nombre FROM usuarios ORDER BY nombre ASC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener trabajadores: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def buscartrabajador(trabajador):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_buscar = """SELECT userid, username, nombre, telefono, rfc, email, direccion, estado, rango
                        FROM usuarios 
                        WHERE nombre = %s
                        LIMIT 1"""

        cursor.execute(sql_buscar, (trabajador,))
        return cursor.fetchone()

    except Exception as e:
        print(f"Error al buscar trabajador: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def actualizartrabajador(userid, username, nombre, telefono, rfc, direccion, estado, email, password, rango):
    """Actualiza los datos de un trabajador; solo reencripta la contraseña si se ingresó una nueva"""
    if not all([userid, username, nombre, telefono, rfc, direccion, estado, email, rango]):
        return False, "Por favor complete todos los campos obligatorios."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Verificar que el username no esté ocupado por otro usuario
        cursor.execute(
            "SELECT userid FROM usuarios WHERE username = %s AND userid != %s",
            (username, userid)
        )
        if cursor.fetchone():
            return False, "Ese nombre de usuario ya está en uso por otro trabajador."

        if password:
            sal = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), sal).decode('utf-8')
            sql_update = """
                UPDATE usuarios
                SET username = %s, nombre = %s, telefono = %s, rfc = %s,
                    direccion = %s, estado = %s, email = %s, password = %s, rango = %s
                WHERE userid = %s
            """
            valores = (username, nombre, telefono, rfc, direccion, estado, email, password_hash, rango, userid)
        else:
            sql_update = """
                UPDATE usuarios
                SET username = %s, nombre = %s, telefono = %s, rfc = %s,
                    direccion = %s, estado = %s, email = %s, rango = %s
                WHERE userid = %s
            """
            valores = (username, nombre, telefono, rfc, direccion, estado, email, rango, userid)

        cursor.execute(sql_update, valores)
        conexion.commit()
        return True, "Información del trabajador actualizada con éxito."

    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al actualizar trabajador: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def eliminartrabajador(userid):
    """Elimina un trabajador de la base de datos evitando borrar al último administrador"""
    if not userid:
        return False, "No hay ningún trabajador seleccionado."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT rango FROM usuarios WHERE userid = %s LIMIT 1", (userid,))
        usuario = cursor.fetchone()
        if not usuario:
            return False, "El trabajador ya no existe en la base de datos."

        if str(usuario["rango"]).lower() == "admin":
            cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE rango = 'admin'")
            total_admins = cursor.fetchone()["total"]
            if total_admins <= 1:
                return False, "No puede despedir al único administrador activo del sistema."

        cursor.execute("DELETE FROM usuarios WHERE userid = %s", (userid,))
        conexion.commit()
        return True, "Trabajador dado de baja correctamente."

    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al eliminar trabajador: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def asegurar_tabla_movimientos():
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos_inventario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(100),
                tipo ENUM('entrada', 'salida') NOT NULL,
                cantidad INT NOT NULL,
                ganancia DECIMAL(10, 2) DEFAULT 0.00,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conexion.commit()
    except Exception as e:
        print(f"Error al verificar tabla movimientos: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def cambiarstock(codigo, cantidad):
    if not codigo or cantidad is None:
        return False, "Rellene los campos"

    conexion = None
    cursor = None

    try:
        asegurar_tabla_movimientos()
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # 1. Consultar el stock actual y precios buscando por código o código de barras
        sql_verificar = """
            SELECT stock, precio_costo, precio_venta
            FROM productos
            WHERE codigo = %s OR codigobarras = %s
            LIMIT 1
        """
        cursor.execute(sql_verificar, (codigo, codigo))
        producto = cursor.fetchone()

        if not producto:
            return False, f"Producto '{codigo}' no encontrado"

        cant_int = int(cantidad)
        stock_actual = producto["stock"] or 0
        nuevo_stock = stock_actual + cant_int

        if nuevo_stock < 0:
            return False, f"Stock insuficiente (disponible: {stock_actual})"

        # 2. Actualizar el stock en la tabla productos
        sql_update = """
            UPDATE productos
            SET stock = %s
            WHERE codigo = %s OR codigobarras = %s
        """
        cursor.execute(sql_update, (nuevo_stock, codigo, codigo))

        # 3. Registrar el movimiento para el panel de Reportes
        if cant_int > 0:
            cursor.execute(
                "INSERT INTO movimientos_inventario (codigo, tipo, cantidad, ganancia) VALUES (%s, 'entrada', %s, 0)",
                (codigo, cant_int)
            )
        elif cant_int < 0:
            unidades_vendidas = abs(cant_int)
            costo = float(producto.get("precio_costo") or 0)
            venta = float(producto.get("precio_venta") or 0)
            ganancia_op = (venta - costo) * unidades_vendidas
            cursor.execute(
                "INSERT INTO movimientos_inventario (codigo, tipo, cantidad, ganancia) VALUES (%s, 'salida', %s, %s)",
                (codigo, unidades_vendidas, ganancia_op)
            )

        conexion.commit()
        return True, f"Stock actualizado a {nuevo_stock}"

    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error de conexión con la base de datos: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def obtener_datos_reportes():
    """Obtiene KPIs, datos para la gráfica de ganancias y productos con stock bajo"""
    asegurar_tabla_movimientos()
    conexion = None
    cursor = None
    datos = {
        "entrados": 0,
        "vendidos": 0,
        "ganancia_total": 0.0,
        "valor_inventario": 0.0,
        "grafica": [],
        "bajo_stock": []
    }
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # 1. Totales de entradas y salidas registradas
        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN tipo = 'entrada' THEN cantidad ELSE 0 END), 0) AS entrados,
                COALESCE(SUM(CASE WHEN tipo = 'salida' THEN cantidad ELSE 0 END), 0) AS vendidos,
                COALESCE(SUM(CASE WHEN tipo = 'salida' THEN ganancia ELSE 0 END), 0) AS ganancia_ventas
            FROM movimientos_inventario
        """)
        mov = cursor.fetchone() or {}
        datos["entrados"] = int(mov.get("entrados") or 0)
        datos["vendidos"] = int(mov.get("vendidos") or 0)

        # 2. Valor de inventario y ganancia proyectada desde productos
        cursor.execute("""
            SELECT
                COALESCE(SUM(stock), 0) AS stock_total,
                COALESCE(SUM(stock * precio_costo), 0) AS valor_costo,
                COALESCE(SUM(stock * (precio_venta - precio_costo)), 0) AS ganancia_potencial
            FROM productos
        """)
        inv = cursor.fetchone() or {}
        if datos["entrados"] == 0:
            datos["entrados"] = int(inv.get("stock_total") or 0)

        ganancia_ventas = float(mov.get("ganancia_ventas") or 0)
        datos["ganancia_total"] = ganancia_ventas if ganancia_ventas > 0 else float(inv.get("ganancia_potencial") or 0)
        datos["valor_inventario"] = float(inv.get("valor_costo") or 0)

        # 3. Top 6 productos por margen de ganancia para la gráfica
        cursor.execute("""
            SELECT nombre,
                   COALESCE(precio_costo, 0) AS costo,
                   COALESCE(precio_venta, 0) AS venta,
                   COALESCE(precio_venta - precio_costo, 0) AS ganancia
            FROM productos
            ORDER BY ganancia DESC
            LIMIT 6
        """)
        datos["grafica"] = cursor.fetchall()

        # 4. Productos con stock bajo (<= 5)
        cursor.execute("""
            SELECT COALESCE(codigo, codigobarras, '-') AS codigo,
                   nombre,
                   COALESCE(stock, 0) AS stock
            FROM productos
            WHERE COALESCE(stock, 0) <= 5
            ORDER BY stock ASC
            LIMIT 15
        """)
        datos["bajo_stock"] = cursor.fetchall()

        return datos
    except Exception as e:
        print(f"Error al obtener reportes: {e}")
        return datos
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

######################## PROVEEDORES ########################

def guardarprovedor(nombre, telefono, rfc, email, direccion, estado):
    """Registra un nuevo proveedor en la base de datos"""
    if not all([nombre, telefono, rfc, email, direccion, estado]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT id FROM proveedores WHERE nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El proveedor ya está registrado."

        sql_insert = """
            INSERT INTO proveedores (nombre, telefono, rfc, email, direccion, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (nombre, telefono, rfc, email, direccion, estado)

        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Proveedor registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def buscarprovedor(provedor):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_buscar = """SELECT id, nombre, telefono, rfc, email, direccion, estado 
                        FROM proveedores 
                        WHERE nombre = %s"""

        cursor.execute(sql_buscar, (provedor,))
        return cursor.fetchone()

    except Exception as e:
        print(f"Error al buscar proveedor: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def obtener_proveedores():
    """Devuelve lista de proveedores (id y nombre) para llenar los ComboBox"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM proveedores ORDER BY nombre ASC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener proveedores: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def obtener_nombre_proveedor(id_proveedor):
    """Devuelve el nombre del proveedor a partir de su ID"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT nombre FROM proveedores WHERE id = %s LIMIT 1", (id_proveedor,))
        fila = cursor.fetchone()
        return fila["nombre"] if fila else None
    except Exception as e:
        print(f"Error al obtener nombre del proveedor: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def actualizarprovedor(id_proveedor, nombre, telefono, rfc, email, direccion, estado):
    """Actualiza los datos de un proveedor existente"""
    if not all([id_proveedor, nombre, telefono, rfc, email, direccion, estado]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql_update = """
            UPDATE proveedores
            SET nombre = %s, telefono = %s, rfc = %s, email = %s, direccion = %s, estado = %s
            WHERE id = %s
        """
        valores = (nombre, telefono, rfc, email, direccion, estado, id_proveedor)
        cursor.execute(sql_update, valores)
        conexion.commit()
        return True, "Datos del proveedor actualizados con éxito."

    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al actualizar proveedor: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

######################## PRODUCTOS ########################

def guardarproducto(marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito, categoria):
    """Registra un nuevo producto en la base de datos"""
    if not all([marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito, categoria]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT id FROM productos WHERE nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El producto ya está registrado."

        sql_insert = """
            INSERT INTO productos (marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito, categoria)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito, categoria)

        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Producto registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def obtener_productos():
    """Devuelve lista de productos (id y nombre) para llenar el ComboBox"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM productos ORDER BY nombre ASC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def buscarproducto_nombre(nombre):
    """Obtiene todos los datos de un producto y el nombre de su proveedor"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT p.id, p.marca, p.nombre, p.codigobarras, p.codigo,
                   p.descripcion, p.precio_costo, p.precio_venta,
                   p.idprovedor, p.requisito, p.categoria,
                   pr.nombre AS nombre_proveedor
            FROM productos p
            LEFT JOIN proveedores pr ON p.idprovedor = pr.id
            WHERE p.nombre = %s
            LIMIT 1
        """
        cursor.execute(sql, (nombre,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar producto: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def actualizarproducto(id_producto, marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito, categoria):
    """Actualiza la información de un producto existente en la base de datos"""
    if not all([id_producto, marca, nombre, codigobarras, codigo, descripcion, precio_costo, precio_venta, idprovedor, requisito, categoria]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # Verificar que no exista otro producto con el mismo nombre
        sql_verificar = "SELECT id FROM productos WHERE nombre = %s AND id != %s"
        cursor.execute(sql_verificar, (nombre, id_producto))
        if cursor.fetchone():
            return False, "Ya existe otro producto registrado con ese nombre."

        sql_update = """
            UPDATE productos
            SET marca = %s,
                nombre = %s,
                codigobarras = %s,
                codigo = %s,
                descripcion = %s,
                precio_costo = %s,
                precio_venta = %s,
                idprovedor = %s,
                requisito = %s,
                categoria = %s
            WHERE id = %s
        """
        valores = (marca, nombre, codigobarras, codigo, descripcion, float(precio_costo), float(precio_venta), idprovedor, requisito, categoria, id_producto,)
        cursor.execute(sql_update, valores)
        conexion.commit()
        return True, "Información del producto actualizada con éxito."

    except ValueError:
        return False, "El costo y el precio de venta deben ser números válidos."
    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al actualizar producto: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
######################## CLIENTES ########################

def guardarcliente(nombre, telefono, rfc, email, direccion, estado, codigo):
    """Registra un nuevo cliente en la base de datos"""
    if not all([nombre, telefono, rfc, email, direccion, estado, codigo]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT id FROM clientes WHERE nombre = %s OR codigo = %s", (nombre, codigo))
        if cursor.fetchone():
            return False, "El nombre o código del cliente ya está registrado."

        sql_insert = """
            INSERT INTO clientes (nombre, codigo, telefono, rfc, estado, direccion, email, puntos, dinerogastado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 0, 0)
        """
        valores = (nombre, codigo, telefono, rfc, estado, direccion, email)
        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Cliente registrado con éxito."

    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def obtener_clientes():
    """Devuelve todos los clientes registrados"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nombre, codigo,
                   COALESCE(puntos, 0) AS puntos,
                   COALESCE(dinerogastado, 0) AS dinerogastado
            FROM clientes
            ORDER BY nombre ASC
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def buscarcliente_nombre(nombre):
    """Obtiene todos los datos de un cliente por su nombre"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nombre, codigo, telefono, rfc, estado, direccion, email,
                   COALESCE(puntos, 0) AS puntos,
                   COALESCE(dinerogastado, 0) AS dinerogastado
            FROM clientes
            WHERE nombre = %s
            LIMIT 1
        """, (nombre,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar cliente: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def actualizarcliente(id_cliente, nombre, telefono, rfc, email, direccion, estado, codigo):
    """Actualiza los datos de un cliente existente"""
    if not all([id_cliente, nombre, telefono, rfc, email, direccion, estado, codigo]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql_update = """
            UPDATE clientes
            SET nombre = %s, codigo = %s, telefono = %s, rfc = %s,
                estado = %s, direccion = %s, email = %s
            WHERE id = %s
        """
        cursor.execute(sql_update, (nombre, codigo, telefono, rfc, estado, direccion, email, id_cliente))
        conexion.commit()
        return True, "Datos del cliente actualizados con éxito."
    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al actualizar cliente: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def buscar_clientes_coincidentes(criterio):
    conexion = obtener_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT id, nombre, codigo,
                   COALESCE(puntos, 0) AS puntos,
                   COALESCE(dinerogastado, 0) AS dinerogastado
            FROM clientes
            WHERE nombre LIKE %s OR CAST(id AS CHAR) LIKE %s OR codigo LIKE %s
            LIMIT 50
        """
        patron = f"%{criterio}%"
        cursor.execute(consulta, (patron, patron, patron))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar clientes: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


def obtener_cliente_por_id(id_cliente=1):
    conexion = obtener_conexion()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT id, nombre, codigo, telefono, rfc, estado, direccion, email,
                   COALESCE(puntos, 0) AS puntos,
                   COALESCE(dinerogastado, 0) AS dinerogastado
            FROM clientes
            WHERE id = %s
            LIMIT 1
        """
        cursor.execute(consulta, (id_cliente,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener cliente: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()


def procesar_puntos_compra(id_cliente, total_compra, canjear=False):
    """
    - Ignora al cliente genérico (id = 1).
    - Si canjear=True, puntos >= 50 y total < 200: resta 50 puntos (compra gratis).
    - En compra normal: suma el monto a dinerogastado y, si total > 200, suma 5 puntos.
    """
    if not id_cliente or int(id_cliente) == 1:
        return True, "Venta a público general (sin movimiento de puntos).", 0

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT COALESCE(puntos, 0) AS puntos, COALESCE(dinerogastado, 0) AS dinerogastado FROM clientes WHERE id = %s LIMIT 1",
            (id_cliente,)
        )
        cliente = cursor.fetchone()
        if not cliente:
            return False, "Cliente no encontrado.", 0

        puntos_actuales = int(cliente["puntos"])
        gasto_actual = int(cliente["dinerogastado"])
        total = float(total_compra)

        if canjear:
            if puntos_actuales < 50:
                return False, "El cliente no cuenta con los 50 puntos necesarios.", puntos_actuales
            if total >= 200:
                return False, "El canje gratis solo aplica en compras menores a $200.00.", puntos_actuales

            nuevos_puntos = puntos_actuales - 50
            cursor.execute("UPDATE clientes SET puntos = %s WHERE id = %s", (nuevos_puntos, id_cliente))
            conexion.commit()
            return True, f"Canje aplicado (-50 pts). Puntos restantes: {nuevos_puntos}.", nuevos_puntos

        nuevo_gasto = gasto_actual + int(round(total))
        nuevos_puntos = puntos_actuales + 5 if total > 200 else puntos_actuales

        cursor.execute(
            "UPDATE clientes SET puntos = %s, dinerogastado = %s WHERE id = %s",
            (nuevos_puntos, nuevo_gasto, id_cliente)
        )
        conexion.commit()

        if total > 200:
            return True, f"¡El cliente ganó +5 puntos! Total acumulado: {nuevos_puntos} pts.", nuevos_puntos
        return True, f"Compra registrada. Puntos actuales: {nuevos_puntos} pts.", nuevos_puntos

    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al actualizar puntos: {e}", 0
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

######################## VENTAS & BÚSQUEDAS ########################
def obtener_producto_de_proveedor(codigo, id_proveedor):
    """Verifica que el producto exista y pertenezca al proveedor activo"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT codigo, codigobarras, nombre, descripcion, idprovedor
            FROM productos
            WHERE (codigo = %s OR codigobarras = %s)
              AND idprovedor = %s
            LIMIT 1
        """
        cursor.execute(sql, (codigo, codigo, id_proveedor))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al verificar producto del proveedor: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def buscar_producto_por_codigo(codigo):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT codigo, codigobarras, nombre, descripcion, precio_venta, stock, requisito, categoria
            FROM productos
            WHERE codigo = %s OR codigobarras = %s
            LIMIT 1
        """
        cursor.execute(sql, (codigo, codigo))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar producto: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def revisar_stock(codigo):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT stock FROM productos WHERE codigo = %s OR codigobarras = %s LIMIT 1"
        cursor.execute(sql, (codigo, codigo))
        fila = cursor.fetchone()
        if fila is None:
            return None
        return fila["stock"] if fila["stock"] is not None else 0
    except Exception as e:
        print(f"Error al revisar stock: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def buscar_productos_coincidentes(criterio):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        query = """
            SELECT p.codigobarras, p.nombre, p.stock, p.precio_venta,
                   COALESCE(pr.nombre, 'Sin proveedor') AS proveedor
            FROM productos p
            LEFT JOIN proveedores pr ON p.idprovedor = pr.id
            WHERE p.codigobarras LIKE %s OR p.nombre LIKE %s
            LIMIT 20
        """
        patron = f"%{criterio}%"
        cursor.execute(query, (patron, patron))
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"No se encontró el producto: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def buscar_productos_por_proveedor(criterio, id_proveedor):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        query = """
            SELECT codigobarras, nombre, stock, precio_venta 
            FROM productos 
            WHERE (codigobarras LIKE %s OR nombre LIKE %s)
              AND idprovedor = %s
            LIMIT 20
        """
        patron = f"%{criterio}%"
        cursor.execute(query, (patron, patron, id_proveedor))
        
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"Error en búsqueda por proveedor: {e}")
        return []

def buscar_proveedores_coincidentes(criterio):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        query = """
            SELECT id, nombre, telefono 
            FROM proveedores 
            WHERE nombre LIKE %s OR rfc LIKE %s
            LIMIT 20
        """
        patron = f"%{criterio}%"
        cursor.execute(query, (patron, patron))

        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"No se encontró el proveedor: {e}")
        return []

def buscar_clientes_coincidentes(criterio):
    conexion = obtener_conexion()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT id, nombre, codigo,
                   COALESCE(puntos, 0) AS puntos,
                   COALESCE(dinerogastado, 0) AS dinerogastado
            FROM clientes
            WHERE nombre LIKE %s OR CAST(id AS CHAR) LIKE %s OR codigo LIKE %s
            LIMIT 50
        """
        patron = f"%{criterio}%"
        cursor.execute(consulta, (patron, patron, patron))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar clientes: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()


def obtener_cliente_por_id(id_cliente=1):
    conexion = obtener_conexion()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT id, nombre, codigo, telefono, rfc, estado, direccion, email,
                   COALESCE(puntos, 0) AS puntos,
                   COALESCE(dinerogastado, 0) AS dinerogastado
            FROM clientes
            WHERE id = %s
            LIMIT 1
        """
        cursor.execute(consulta, (id_cliente,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener cliente: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()


def procesar_puntos_compra(id_cliente, total_compra, canjear=False):
    """
    Aplica las reglas de puntos y actualiza dinerogastado:
    - Ignora al cliente genérico (id = 1).
    - Si canjear=True, puntos >= 50 y total < 200: descuenta 50 puntos y no suma gasto.
    - En compra normal: suma el monto a dinerogastado y, si total > 200, suma 5 puntos.
    """
    if not id_cliente or int(id_cliente) == 1:
        return True, "Venta a público general (sin movimiento de puntos).", 0

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT COALESCE(puntos, 0) AS puntos, COALESCE(dinerogastado, 0) AS dinerogastado FROM clientes WHERE id = %s LIMIT 1",
            (id_cliente,)
        )
        cliente = cursor.fetchone()
        if not cliente:
            return False, "Cliente no encontrado.", 0

        puntos_actuales = int(cliente["puntos"])
        gasto_actual = int(cliente["dinerogastado"])
        total = float(total_compra)

        # 1. Canje de 50 puntos en compra menor a $200
        if canjear:
            if puntos_actuales < 50:
                return False, "El cliente no cuenta con los 50 puntos necesarios.", puntos_actuales
            if total >= 200:
                return False, "El canje gratis solo aplica en compras menores a $200.00.", puntos_actuales

            nuevos_puntos = puntos_actuales - 50
            cursor.execute(
                "UPDATE clientes SET puntos = %s WHERE id = %s",
                (nuevos_puntos, id_cliente)
            )
            conexion.commit()
            return True, f"Canje aplicado (-50 pts). Puntos restantes: {nuevos_puntos}.", nuevos_puntos

        # 2. Compra normal: acumula dinerogastado y suma 5 puntos si supera $200
        nuevo_gasto = gasto_actual + int(round(total))
        nuevos_puntos = puntos_actuales + 5 if total > 200 else puntos_actuales

        cursor.execute(
            "UPDATE clientes SET puntos = %s, dinerogastado = %s WHERE id = %s",
            (nuevos_puntos, nuevo_gasto, id_cliente)
        )
        conexion.commit()

        if total > 200:
            return True, f"¡El cliente ganó +5 puntos! Total acumulado: {nuevos_puntos} pts.", nuevos_puntos
        return True, f"Compra registrada. Puntos actuales: {nuevos_puntos} pts.", nuevos_puntos

    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al actualizar puntos: {e}", 0
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

########################################## PROMOCIONES

def obtener_detalle_producto(codigo):
    """Busca un producto por código o código de barras e incluye su requisito y categoría"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT codigo, codigobarras, nombre, precio_venta,
                   COALESCE(requisito, 'Ninguno') AS requisito,
                   COALESCE(categoria, 'Sin limitaciones') AS categoria
            FROM productos
            WHERE codigo = %s OR codigobarras = %s
            LIMIT 1
        """
        cursor.execute(sql, (codigo, codigo))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar detalle de producto: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def validar_compatibilidad_promocion(codigos):
    """Verifica que los productos de una promoción no estén repetidos ni tengan condiciones incompatibles"""
    codigos_validos = [c for c in codigos if c]
    if not codigos_validos:
        return False, "Debe agregar al menos un producto a la promoción."

    productos = []
    ids_vistos = set()

    for cod in codigos_validos:
        prod = obtener_detalle_producto(cod)
        if not prod:
            return False, f"El producto '{cod}' no existe en la base de datos."

        clave_unica = prod.get("codigo") or prod.get("codigobarras") or str(cod)
        if clave_unica in ids_vistos:
            return False, f"El producto '{prod['nombre']}' está repetido. Use el campo Cantidad para agregar más unidades."
        ids_vistos.add(clave_unica)

        requisito = str(prod.get("requisito") or "Ninguno").strip()
        categoria = str(prod.get("categoria") or "Sin limitaciones").strip()

        if requisito in ("Receta", "Identificación") or categoria == "Limitado":
            return False, (
                f"'{prod['nombre']}' no es compatible con promociones "
                f"(Requisito: {requisito} | Categoría: {categoria})."
            )

        productos.append(prod)

    # Verificar que todos compartan exactamente el mismo requisito y categoría
    req_base = str(productos[0].get("requisito") or "Ninguno").strip()
    cat_base = str(productos[0].get("categoria") or "Sin limitaciones").strip()

    for prod in productos[1:]:
        req_actual = str(prod.get("requisito") or "Ninguno").strip()
        cat_actual = str(prod.get("categoria") or "Sin limitaciones").strip()
        if req_actual != req_base or cat_actual != cat_base:
            return False, (
                f"Productos incompatibles: '{productos[0]['nombre']}' ({req_base} / {cat_base}) "
                f"no se puede combinar con '{prod['nombre']}' ({req_actual} / {cat_actual})."
            )

    return True, "Productos compatibles."


def guardarpromocion(nombre, fproducto, fcantidad, sproducto, scantidad, tproducto, tcantidad, precio):
    if not all([nombre, fproducto, fcantidad, precio]):
        return False, "Complete al menos el nombre, el primer producto, su cantidad y el precio."

    compatible, msg_compat = validar_compatibilidad_promocion([fproducto, sproducto, tproducto])
    if not compatible:
        return False, msg_compat

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT id FROM promocion WHERE nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "Ya existe una promoción registrada con ese nombre."

        sql_insert = """
            INSERT INTO promocion (nombre, fproducto, fcantidad, sproducto, scantidad, tproducto, tcantidad, precio)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            nombre,
            fproducto,
            int(fcantidad),
            sproducto if sproducto else None,
            int(scantidad) if scantidad else None,
            tproducto if tproducto else None,
            int(tcantidad) if tcantidad else None,
            float(precio)
        )
        cursor.execute(sql_insert, valores)
        conexion.commit()
        return True, "Promoción registrada con éxito."

    except ValueError:
        return False, "Las cantidades deben ser números enteros y el precio un número válido."
    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error de conexión con la base de datos: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def obtener_promociones():
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, activo FROM promocion ORDER BY id DESC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener promociones: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def cambiar_estado_promocion(promo_id, activo):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        sql = "UPDATE promocion SET activo = %s WHERE id = %s"
        cursor.execute(sql, (activo, promo_id))
        conexion.commit()
        return True, "Estado de la promoción actualizado."
    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al actualizar estado: {e}"
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def obtener_email_proveedor(id_proveedor):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT nombre, email FROM proveedores WHERE id = %s LIMIT 1",
            (id_proveedor,),
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener correo del proveedor: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def obtener_promociones_completas():
    """Devuelve todas las promociones junto con los nombres y precios regulares de sus productos"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT pr.id, pr.nombre,
                   pr.fproducto, pr.fcantidad,
                   pr.sproducto, pr.scantidad,
                   pr.tproducto, pr.tcantidad,
                   pr.precio, pr.activo,
                   p1.nombre AS nombre_p1, COALESCE(p1.precio_venta, 0) AS precio_p1,
                   p2.nombre AS nombre_p2, COALESCE(p2.precio_venta, 0) AS precio_p2,
                   p3.nombre AS nombre_p3, COALESCE(p3.precio_venta, 0) AS precio_p3
            FROM promocion pr
            LEFT JOIN productos p1 ON (pr.fproducto = p1.codigo OR pr.fproducto = p1.codigobarras)
            LEFT JOIN productos p2 ON (pr.sproducto = p2.codigo OR pr.sproducto = p2.codigobarras)
            LEFT JOIN productos p3 ON (pr.tproducto = p3.codigo OR pr.tproducto = p3.codigobarras)
            ORDER BY pr.id DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener promociones completas: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def eliminarpromocion(promo_id):
    """Elimina una promoción de la base de datos por su ID"""
    if not promo_id:
        return False, "Seleccione una promoción válida."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM promocion WHERE id = %s", (promo_id,))
        conexion.commit()
        return True, "Promoción eliminada correctamente."
    except Exception as e:
        if conexion:
            conexion.rollback()
        return False, f"Error al eliminar promoción: {e}"
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
def obtener_producto_con_proveedor(codigo):
    """Busca un producto por código o código de barras junto con el nombre de su proveedor"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT p.codigo, p.codigobarras, p.nombre, p.descripcion,
                     p.idprovedor,
                   COALESCE(pr.nombre, 'Sin proveedor') AS nombre_proveedor
            FROM productos p
            LEFT JOIN proveedores pr ON p.idprovedor = pr.id
            WHERE p.codigo = %s OR p.codigobarras = %s
            LIMIT 1
        """
        cursor.execute(sql, (codigo, codigo))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar producto con proveedor: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()