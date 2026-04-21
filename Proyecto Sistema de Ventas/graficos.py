import mysql.connector
import matplotlib.pyplot as plt

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ventas_db"
    )

def grafico_ventas_por_cliente():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT c.nombre, SUM(p.precio * dv.cantidad)
    FROM clientes c
    JOIN ventas v ON c.id = v.cliente_id
    JOIN detalle_ventas dv ON v.id = dv.venta_id
    JOIN productos p ON dv.producto_id = p.id
    GROUP BY c.nombre
    """

    cursor.execute(sql)
    datos = cursor.fetchall()

    nombres = [d[0] for d in datos]
    ventas = [d[1] for d in datos]

    plt.bar(nombres, ventas)
    plt.title("Ventas por Cliente")
    plt.xlabel("Clientes")
    plt.ylabel("Total ventas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def grafico_productos():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT p.nombre, SUM(dv.cantidad)
    FROM productos p
    JOIN detalle_ventas dv ON p.id = dv.producto_id
    GROUP BY p.nombre
    """

    cursor.execute(sql)
    datos = cursor.fetchall()

    nombres = [d[0] for d in datos]
    cantidades = [d[1] for d in datos]

    plt.bar(nombres, cantidades, color="green")
    plt.title("Productos mas vendidos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
