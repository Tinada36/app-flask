import os
import psycopg2
from psycopg2 import Error
from flask import Flask, request, render_template

app = Flask(__name__)

connection = None
DATABASE_URL = os.getenv('DATABASE_URL')

@app.route('/')
def index():
    return render_template('index.html')

def create_table():
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute("""
    CREATE TABLE info_people (
        peopleid INT PRIMARY KEY,
        peoplename VARCHAR(100),
        peopleemail VARCHAR(255),
        peoplephone INT
    );
    """)
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL: ", error)
    finally:
        cursor.close()
        connection.close()
        #print("Соединение закрыто")

@app.route('/submit', methods=['POST'])
def insert_to_db():
    name = request.form['name']
    id = request.form['id']
    email = request.form['email']
    phone = request.form['phone']

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    """ins_data = input("Введите данные для добавления (id, name, email, phone): ").split()"""
    cursor.execute(f"INSERT INTO info_people (peopleid, peoplename, peopleemail, peoplephone) VALUES ('{id}', '{name}', '{email}', '{phone}');")
    connection.commit()
    cursor.close()
    connection.close()
    return render_template('index.html', name=name, id=id, email=email, phone=phone)
        #print("Соединение с PostgreSQL закрыто")
@app.route('/data')
def select_from_db():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    """sel_data = input("Выберите столбец для получения информации (name, email, phone или *): ")
        if sel_data == "*":
            cursor.execute(f"SELECT {sel_data} FROM info_people;")
        else:
            cursor.execute(f"SELECT people{sel_data} FROM info_people;")
        data = cursor.fetchall()
        for row in data:
            print(row)
        print("Команда успешно выполнена")"""
    cursor.execute("SELECT * FROM info_people;")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
        #print("Соединение с PostgreSQL закрыто")
    return render_template('data.html', rows=rows)

def main():
    create_table()
    app.run(host='0.0.0.0', port=5000)
    """while True:
        ent = int(input(":"))
        if ent == 1:
            insert_to_db()
        elif ent == 2:
            select_from_db()
        elif ent == 3:
            break
        else:
            print("Вы ввели не верное значение")"""
if __name__ == '__main__':
    main()
