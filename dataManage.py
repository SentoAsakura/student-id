import sqlite3 as sql
from check import logTime

connection = sql.connect('database.db')
print('Successfully connect to database')

cursor = connection.cursor()

def find_n_update(id):
    status = logTime().state
    
    try:
        cursor.execute(f"""UPDATE student SET state = '{status}',time = datetime('now','localtime') WHERE id = {id}""")
        connection.commit()
        
    finally:
        cursor.execute(f"""SELECT * FROM student WHERE id = {id}""")
        items = cursor.fetchall()
        if len(items) == 0:
            print('Học sinh không tồn tại')
        for item in items:
            print(item)

def history():
    cursor.execute("SELECT * FROM student ORDER BY time DESC LIMIT 5")
    items = cursor.fetchall()
    for item in items:
        print(f'{item[1]} {item[2]}')
find_n_update(1)
history()