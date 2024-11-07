import sqlitecloud as sql
from check import logTime
from datetime import datetime, timezone

connection = sql.connect('sqlitecloud://ca5rcloqsz.sqlite.cloud:8860?apikey=tlareWaPX2WwzzKjAwjBpkQxIcV1HsFR4Im5rM4fX0g')
print('Successfully connect to database')

connection.execute('USE DATABASE database.sqlite')

cursor = connection.cursor()

def find_n_update(id:int):
    status = logTime().state
    new_late = 0
    cursor.execute(f'SELECT absent FROM student where id = {id}')
    curr_late : int = int(cursor.fetchone()[0]) | 0
    if status == "Trễ":
        if curr_late:
            new_late = int(curr_late) + 1
        
    else: 
        new_late = int(curr_late)
    
    try:
        newCurr = connection.cursor()
        newCurr.execute(f"""UPDATE student SET state = '{status}',time = datetime('{datetime.now()}'),absent = {new_late} WHERE id = {id}""")
        connection.commit()
        cursor.execute(f"""SELECT * FROM student WHERE id = {id}""")
    except:
        print('An error occured')
    finally:
        items = cursor.fetchall()
        if len(items) == 0:
            print('Học sinh không tồn tại')
        for item in items:
            print(item)

def history():
    his_cursor = connection.cursor()
    his_cursor.execute("SELECT * FROM history ORDER BY time DESC LIMIT 5")
    items = his_cursor.fetchall()
    log = ""
    for item in items:
        log+= f'{" ".join(item)}\n\n'
    #print(log)
    return log

if __name__ == '__main__':
    find_n_update(99)
    print(history())