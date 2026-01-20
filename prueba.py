import mysql.connector
from mysql.connector import Error

print("Iniciando prueba MySQL...")

try:
    conexion = mysql.connector.connect(
        host="127.0.0.1",    # importante usar 127.0.0.1
        port=3306,           # asegúrate que sea el puerto correcto
        user="root",         # usuario XAMPP
        password="",         # contraseña vacía XAMPP por defecto
        database="agenda_web",
        connect_timeout=5    # evita quedarse colgado
    )
    print("hola1")

    if conexion.is_connected():
        print("✅ Conexión MySQL exitosa")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuario LIMIT 1")
        print(cursor.fetchall())

except Error as e:
    print("❌ Error al conectar a MySQL:", e)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()

print("Test finalizado")
