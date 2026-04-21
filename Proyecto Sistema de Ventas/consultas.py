import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ventas_db"
    )

def ver_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes")
    data = cursor.fetchall()

    conn.close()
    return data

def ver_productos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    data = cursor.fetchall()

    conn.close()
    return data

def ver_ventas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ventas")
    resultados = cursor.fetchall()

    print("\n💰 VENTAS:")
    for r in resultados:
        print(r)

    conn.close()

def ventas_por_cliente():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT c.nombre, SUM(p.precio * dv.cantidad) AS total
    FROM clientes c
    JOIN ventas v ON c.id = v.cliente_id
    JOIN detalle_ventas dv ON v.id = dv.venta_id
    JOIN productos p ON dv.producto_id = p.id
    GROUP BY c.nombre
    """

    cursor.execute(sql)
    data = cursor.fetchall()

    conn.close()
    return data

def productos_mas_vendidos():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT p.nombre, SUM(dv.cantidad) AS total_vendido
    FROM productos p
    JOIN detalle_ventas dv ON p.id = dv.producto_id
    GROUP BY p.nombre
    ORDER BY total_vendido DESC
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    print("\n🏆 PRODUCTOS MÁS VENDIDOS:")
    for r in resultados:
        print(f"{r[0]} -> {r[1]} unidades")

    conn.close()


def ingreso_total():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT SUM(p.precio * dv.cantidad)
    FROM detalle_ventas dv
    JOIN productos p ON dv.producto_id = p.id
    """

    cursor.execute(sql)
    total = cursor.fetchone()[0]

    conn.close()
    return total

def promedio_venta():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT AVG(total)
    FROM (
        SELECT SUM(p.precio * dv.cantidad) AS total
        FROM detalle_ventas dv
        JOIN productos p ON dv.producto_id = p.id
        GROUP BY dv.venta_id
    ) AS ventas
    """

    cursor.execute(sql)
    resultado = cursor.fetchone()[0]

    conn.close()
    return resultado

def mejor_cliente():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT c.nombre, SUM(p.precio * dv.cantidad) AS total
    FROM clientes c
    JOIN ventas v ON c.id = v.cliente_id
    JOIN detalle_ventas dv ON v.id = dv.venta_id
    JOIN productos p ON dv.producto_id = p.id
    GROUP BY c.nombre
    ORDER BY total DESC
    LIMIT 1
    """

    cursor.execute(sql)
    data = cursor.fetchone()

    conn.close()
    return data

def producto_estrella():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT p.nombre, SUM(dv.cantidad) AS total
    FROM productos p
    JOIN detalle_ventas dv ON p.id = dv.producto_id
    GROUP BY p.nombre
    ORDER BY total DESC
    LIMIT 1
    """

    cursor.execute(sql)
    data = cursor.fetchone()

    conn.close()
    return data

def ventas_hoy():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(p.precio * dv.cantidad), 0)
        FROM ventas v
        JOIN detalle_ventas dv ON v.id = dv.venta_id
        JOIN productos p ON dv.producto_id = p.id
        WHERE DATE(v.fecha) = CURDATE()
    """)

    total = cursor.fetchone()[0]
    conn.close()
    return total

def top_productos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.nombre, SUM(dv.cantidad) AS total
        FROM productos p
        JOIN detalle_ventas dv ON p.id = dv.producto_id
        GROUP BY p.nombre
        ORDER BY total DESC
        LIMIT 5
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def top_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.nombre, SUM(p.precio * dv.cantidad) AS total
        FROM clientes c
        JOIN ventas v ON c.id = v.cliente_id
        JOIN detalle_ventas dv ON v.id = dv.venta_id
        JOIN productos p ON dv.producto_id = p.id
        GROUP BY c.nombre
        ORDER BY total DESC
        LIMIT 5
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def ultimas_ventas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.id, c.nombre, v.fecha,
               SUM(p.precio * dv.cantidad) AS total
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN detalle_ventas dv ON v.id = dv.venta_id
        JOIN productos p ON dv.producto_id = p.id
        GROUP BY v.id
        ORDER BY v.id DESC
        LIMIT 5
    """)

    data = cursor.fetchall()
    conn.close()
    return data
