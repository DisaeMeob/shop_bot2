import sqlite3

def create_table():
    conn = sqlite3.connect('iyoka_users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER UNIQUE)")
    conn.commit()
    conn.close()

def add_user(telegram_id):
    conn = sqlite3.connect('iyoka_users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users(telegram_id) VALUES(?)", (telegram_id,))
    conn.commit()
    conn.close()

def exists(telegram_id):
    conn = sqlite3.connect("iyoka_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id=?",(telegram_id,))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    
def get_users():
    conn = sqlite3.connect('iyoka_users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM users")
    users = cursor.fetchall()
    return [user[0] for user in users]

def get_stat():
  conn = sqlite3.connect('iyoka_users.db')
  cursor = conn.cursor()
  cursor.execute("SELECT telegram_id FROM users")
  result = cursor.fetchall()
  conn.close()
  return result