import sqlite3

def init_db():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    
    # 1. Таблиця Юзерів
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, balance REAL)''')
    
    # 2. Таблиця Тікетів (для XSS)
    c.execute('''CREATE TABLE IF NOT EXISTS tickets 
                 (id INTEGER PRIMARY KEY, content TEXT)''')

    # Додаємо адміна і жертву
    c.execute("INSERT OR IGNORE INTO users (id, username, password, balance) VALUES (1, 'admin', 'SuperSecretPass123', 1000000)")
    c.execute("INSERT OR IGNORE INTO users (id, username, password, balance) VALUES (2, 'user', '123456', 50)")
    
    conn.commit()
    conn.close()
    print("✅ Database 'bank.db' initialized with dummy data.")

if __name__ == '__main__':
    init_db()
