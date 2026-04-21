import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ventas_db"
    )

def agregar_cliente(nombre, ciudad):
    conn = conectar()
    cursor = conn.cursor()

    sql = "INSERT INTO clientes (nombre, ciudad) VALUES (%s, %s)"
    valores = (nombre, ciudad)

    cursor.execute(sql, valores)
    conn.commit()

    print("Cliente agregado ✅")

    conn.close()
