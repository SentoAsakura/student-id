import sqlitecloud as sql
from check import logTime

connection = sql.connect('sqlitecloud://ca5rcloqsz.sqlite.cloud:8860?apikey=tlareWaPX2WwzzKjAwjBpkQxIcV1HsFR4Im5rM4fX0g')
print('Successfully connect to database')

connection.execute('USE DATABASE database.db')

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
    his_cursor = connection.cursor()
    his_cursor.execute("SELECT * FROM student ORDER BY time DESC LIMIT 5")
    items = his_cursor.fetchall()
    for item in items:
        print(f'{item[1]} {item[2]}')
find_n_update(1)
history()