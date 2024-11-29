import sqlite3

def initiate_db():
    connection = sqlite3.connect('Base.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                age INT NOT NULL,
                balance INT NOT NULL
                );
            ''')
    cursor.execute("CREATE INDEX idx_email ON Users(email)")

    for i in range(1, 5):
         cursor.execute("INSERT INTO Products (id, title, description, price) VALUES(?, ?, ?, ?)",
                        (i, f"Продукт {i}", f"Описание {i}", f" {i * 100}"))
    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect('Base.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f"{username}", f"{email}", f"{age}", f"1000"))
    connection.commit()



def is_included(username):
    connection = sqlite3.connect('Base.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?',(username,))
    connection.commit()
    if check_user.fetchone() is None:
        return False
    else:
        return True



def get_all_products():
    connection = sqlite3.connect('Base.db')
    cursor = connection.cursor()
    all_prod = cursor.execute('SELECT * FROM Products')
    all_prod = cursor.fetchall()
    return list(all_prod)


# ft=get_all_products(1)
# print(ft)
