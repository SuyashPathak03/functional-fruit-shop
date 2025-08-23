# shop/db_utils.py
import MySQLdb

def get_stock_data():
    conn = MySQLdb.connect(
        host="SuyashPathak.mysql.pythonanywhere-services.com",
        user="SuyashPathak",
        passwd="Suyash_12",   # use your actual password
        db="SuyashPathak$default"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks;")
    stock = cursor.fetchall()
    cursor.close()
    conn.close()
    return stock

def get_stock_for_fruit(fruit_name):
    """Return available quantity for a given fruit name"""
    conn = MySQLdb.connect(
        host="SuyashPathak.mysql.pythonanywhere-services.com",
        user="SuyashPathak",
        passwd="Suyash_12",
        db="SuyashPathak$default"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT available_qty FROM stocks WHERE fruit_name = %s", (fruit_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]  # available_qty
    return 0
