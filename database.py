
import mysql.connector
from mysql.connector import Error

def connect_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="attendance_app",
            password="NotNewPass123!",
            database="attendance_management"
        )

        if connection.is_connected():
            print("Database connected successfully!")
            return connection

    except Error as e:
        print("Database connection failed:", e)

    return None
