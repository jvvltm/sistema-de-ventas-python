import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ventas_db"
)

cursor = conn.cursor()

sql = "INSERT INTO clientes (nombre, ciudad) VALUES (%s, %s)"
valores = ("Juan Pérez", "Antofagasta")

cursor.execute(sql, valores)

conn.commit()

print("Cliente insertado correctamente ✅")

conn.close()
