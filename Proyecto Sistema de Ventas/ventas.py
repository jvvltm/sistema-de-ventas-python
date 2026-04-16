import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1q2w3e4r",
        database="ventas_db"
    )

def crear_venta(cliente_id, fecha):
    conn = conectar()
    cursor = conn.cursor()

    sql = "INSERT INTO ventas (cliente_id, fecha) VALUES (%s, %s)"
    cursor.execute(sql, (cliente_id, fecha))

    conn.commit()
    venta_id = cursor.lastrowid

    conn.close()
    return venta_id


def agregar_detalle(venta_id, producto_id, cantidad):
    conn = conectar()
    cursor = conn.cursor()

    sql = "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad) VALUES (%s, %s, %s)"
    cursor.execute(sql, (venta_id, producto_id, cantidad))

    conn.commit()
    conn.close()

    print("Detalle agregado ✅")

def obtener_total_venta(venta_id):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT SUM(p.precio * dv.cantidad)
    FROM detalle_ventas dv
    JOIN productos p ON dv.producto_id = p.id
    WHERE dv.venta_id = %s
    """

    cursor.execute(sql, (venta_id,))
    resultado = cursor.fetchone()[0]

    conn.close()
    return resultado

def obtener_detalle_boleta(venta_id):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT p.nombre, dv.cantidad, p.precio, (p.precio * dv.cantidad) AS subtotal
    FROM detalle_ventas dv
    JOIN productos p ON dv.producto_id = p.id
    WHERE dv.venta_id = %s
    """

    cursor.execute(sql, (venta_id,))
    data = cursor.fetchall()

    conn.close()
    return data

def imprimir_boleta(venta_id):
    from ventas import obtener_detalle_boleta

    datos = obtener_detalle_boleta(venta_id)

    print("\n" + "="*40)
    print("🧾 BOLETA DE COMPRA")
    print("="*40)

    total = 0

    for nombre, cantidad, precio, subtotal in datos:
        print(f"{nombre} x{cantidad} - ${subtotal}")
        total += subtotal

    print("="*40)
    print(f"💰 TOTAL: ${total}")
    print("="*40)

def obtener_boleta(venta_id):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    SELECT p.nombre, dv.cantidad, p.precio, (p.precio * dv.cantidad)
    FROM detalle_ventas dv
    JOIN productos p ON dv.producto_id = p.id
    WHERE dv.venta_id = %s
    """

    cursor.execute(sql, (venta_id,))
    data = cursor.fetchall()

    conn.close()
    return data



def exportar_boleta_pdf(venta_id, datos, total):
    archivo = f"boleta_{venta_id}.pdf"

    c = canvas.Canvas(archivo, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "BOLETA DE COMPRA")

    y = 700
    c.setFont("Helvetica", 12)

    for nombre, cant, precio, subtotal in datos:
        linea = f"{nombre} x{cant} = ${subtotal}"
        c.drawString(100, y, linea)
        y -= 20

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y-20, f"TOTAL: ${total}")

    c.save()

    return archivo