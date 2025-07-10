import sqlite3

def create_table_order():
    conn = sqlite3.connect('in_order.db')
    cursor = conn.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS orders(
                    name TEXT UNIQUE,
                    price INTEGER,
                    photo TEXT        
)
''')
    conn.commit()
    conn.close()

    
def add_order(name,price,photo):
    conn = sqlite3.connect('in_order.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders VALUES(?,?,?)',(name,price,photo))
    conn.commit()
    conn.close()

def exist_order(name):
    conn = sqlite3.connect('in_order.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE name = ?',(name,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    
def delete_order(name):
    conn = sqlite3.connect('in_order.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orders WHERE name = ?', (name,))
    conn.commit()
    conn.close()


def create_stock():
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS stock(
                   name TEXT UNIQUE,
                   price INTEGER,
                   photo TEXT)''')
    

def add_stock(name,price,photo):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO stock VALUES(?,?,?)',(name,price,photo))
    conn.commit()
    conn.close()

def exist_stock(name):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock WHERE name = ?',(name,))
    result = cursor.fetchone()
    print("Проверка exist_stock для:", name)
    if result:
        return True
        
    else:
        return False
    

def delete_stock(name):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM stock WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def get_stock_name(name):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, price FROM stock WHERE name = ?', (name,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        return None
    

def get_order_name(name):
    conn = sqlite3.connect('in_order.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, price FROM orders WHERE name = ?', (name,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        return None
    
def get_order_photo(name):
    conn = sqlite3.connect('in_order.db')
    cursor = conn.cursor()
    cursor.execute('SELECT photo FROM orders WHERE name = ?',(name,))
    photo = cursor.fetchone()
    if photo:
        return photo[0]
    else:
        return None
    
def get_stock_photo(name):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('SELECT photo FROM stock WHERE name = ?',(name,))
    photo = cursor.fetchone()
    if photo:
        return photo[0]
    else:
        return None
    
def update_order(cost,photo,name):
    conn = sqlite3.connect('in_order.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE orders SET price = ?, photo = ? WHERE name = ?',(cost,photo,name))
    conn.commit()
    conn.close()

def update_stock(cost,photo,name):
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE stock SET price = ?, photo = ? WHERE name = ?',(cost,photo,name))