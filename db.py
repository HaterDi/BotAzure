import pyodbc
from config import SQL_CONNECTION_STRING

def get_connection():
    return pyodbc.connect(SQL_CONNECTION_STRING)

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users')
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            first_name NVARCHAR(50),
            last_name NVARCHAR(50),
            birth_date DATE,
            email NVARCHAR(100),
            phone NVARCHAR(20),
            street NVARCHAR(100),
            house_number NVARCHAR(20),
            zip_code NVARCHAR(20),
            city NVARCHAR(50),
            country NVARCHAR(50)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_user(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (first_name, last_name, birth_date, email, phone, street, house_number, zip_code, city, country)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user['first_name'],
        user['last_name'],
        user['birth_date'],
        user['email'],
        user['phone'],
        user['street'],
        user['house_number'],
        user['zip_code'],
        user['city'],
        user['country']
    ))
    conn.commit()
    cursor.close()
    conn.close()
