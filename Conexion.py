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

def cambiarstock(codigo, cantidad):
    if not codigo or cantidad is None:
        return False, "Rellene los campos"

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        # 1. Consultar el stock actual buscando por código o código de barras
        sql_verificar = """
            SELECT stock
            FROM productos
            WHERE codigo = %s OR codigobarras = %s
            LIMIT 1
        """
        cursor.execute(sql_verificar, (codigo, codigo))
        producto = cursor.fetchone()

        if not producto:
            return False, f"Producto '{codigo}' no encontrado"

        stock_actual = producto["stock"] or 0
        nuevo_stock = stock_actual + int(cantidad)

        if nuevo_stock < 0:
            return False, f"Stock insuficiente (disponible: {stock_actual})"

        # 2. Actualizar el registro existente en la base de datos
        sql_update = """
            UPDATE productos
            SET stock = %s
            WHERE codigo = %s OR codigobarras = %s
        """
        cursor.execute(sql_update, (nuevo_stock, codigo, codigo))
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

def guardarcliente(nombre, telefono, rfc, email, direccion, estado, username):
    """Registra un nuevo cliente en la base de datos"""
    if not all([nombre, telefono, rfc, email, direccion, estado, username]):
        return False, "Por favor complete todos los campos."

    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        sql_verificar = "SELECT id FROM clientes WHERE nombre = %s"
        cursor.execute(sql_verificar, (nombre,))
        if cursor.fetchone():
            return False, "El cliente ya está registrado."

        sql_insert = """
            INSERT INTO clientes (nombre, telefono, rfc, email, direccion, estado, username)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nombre, telefono, rfc, email, direccion, estado, username)

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


def buscar_producto_por_codigo(codigo, codigobarras):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT codigo, codigobarras FROM productos WHERE codigo = %s OR codigobarras = %s"
        cursor.execute(sql, (codigo, codigobarras))
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos
    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

def revisar_stock(codigo):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = "SELECT stock FROM productos WHERE codigo = %s"
        cursor.execute(sql, (codigo,))
        stock = cursor.fetchone()
        cursor.close()
        conexion.close()
        return stock
    except Exception as e:
        return False, f"Error de conexión con la base de datos: {str(e)}"

def buscar_productos_coincidentes(criterio):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        query = """
            SELECT codigobarras, nombre, stock, precio_venta 
            FROM productos 
            WHERE codigobarras LIKE %s OR nombre LIKE %s 
            LIMIT 20
        """
        patron = f"%{criterio}%"
        cursor.execute(query, (patron, patron))
        
        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"No se encontró el producto: {e}")
        return []

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
    conexion = obtener_conexion()  # Usa el nombre de tu función de conexión en Conexion.py
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        # Ajusta 'clientes', 'id' o 'nombre' si en tu tabla se llaman distinto (ej. id_cliente)
        consulta = """
            SELECT id, nombre
            FROM clientes
            WHERE nombre LIKE %s OR CAST(id AS CHAR) LIKE %s
            LIMIT 50
        """
        patron = f"%{criterio}%"
        cursor.execute(consulta, (patron, patron))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al buscar clientes: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

def obtener_cliente_por_id(id_cliente=1):
    conexion = obtener_conexion()  # Usa el nombre de tu función de conexión en Conexion.py
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        consulta = """
            SELECT id, nombre, codigo, telefono, rfc, estado, direccion, email
            FROM clientes
            WHERE id = %s
            LIMIT 1
        """
        cursor.execute(consulta, (id_cliente,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener cliente por defecto: {e}")
        return None
    finally:
        cursor.close()
        conexion.close()

########################################## PROMOCIONES

def obtener_detalle_producto(codigo):
    """Busca un solo producto por código o código de barras y devuelve su nombre"""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        sql = """
            SELECT codigo, codigobarras, nombre, precio_venta
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


def guardarpromocion(nombre, fproducto, fcantidad, sproducto, scantidad, tproducto, tcantidad, precio):
    if not all([nombre, fproducto, fcantidad, precio]):
        return False, "Complete al menos el nombre, el primer producto, su cantidad y el precio."

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