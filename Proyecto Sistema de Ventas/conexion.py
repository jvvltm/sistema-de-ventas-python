import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ventas_db"
)

print("Conexión exitosa 🚀")

conn.close()
