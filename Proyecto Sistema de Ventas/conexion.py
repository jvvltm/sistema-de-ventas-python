import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1q2w3e4r",
    database="ventas_db"
)

print("Conexión exitosa 🚀")

conn.close()