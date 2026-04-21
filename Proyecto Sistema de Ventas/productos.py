import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ventas_db"
    )

def agregar_producto(nombre, precio):
    conn = conectar()
    cursor = conn.cursor()

    sql = "INSERT INTO productos (nombre, precio) VALUES (%s, %s)"
    valores = (nombre, precio)

    cursor.execute(sql, valores)
    conn.commit()

    print("Producto agregado ✅")

    conn.close()
