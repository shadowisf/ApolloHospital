from flask import session
import mysql.connector

#database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'apollo_hms',
}

def authenticate_receptionist(username, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM receptionist_user WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return user
        return None
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    finally:
        cursor.close()
        conn.close()

def register_receptionist(username, email, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO receptionist_user (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)
        cursor.execute(insert_query, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    finally:
        cursor.close()
        conn.close()

def authenticate_doctor(username, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM doctor_user WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return user
        return None
    except mysql.connector.Error as err:
        print("Error ", err)
        return False
    finally:
        cursor.close()
        conn.close()

def register_doctor(username, email, password):   
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO doctor_user (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)
        cursor.execute(insert_query, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("Error ", err)
        return False
    finally:
        cursor.close()
        conn.close()

def authenticate_staff(username, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM staff_user WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return user
        return None
    except mysql.connector.Error as err:
        print("Error ", err)
        return False
    finally:
        cursor.close()
        conn.close()

def register_staff(username, email, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        insert_query = "INSERT INTO staff_user (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)
        cursor.execute(insert_query, values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("Error ", err)
        return False
    finally:
        cursor.close()
        conn.close()

