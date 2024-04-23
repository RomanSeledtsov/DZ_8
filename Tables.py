import sqlite3


def create_connection(hw_bd):
    conn = None
    try:
        conn = sqlite3.connect(hw_bd)
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)


sql_countries_table = '''
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    country_title VARCHAR(200) NOT NULL
)
'''

sql_cities_table = '''
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    cities_title VARCHAR(200) NOT NULL,
    area FLOAT(150, 2) NOT NULL DEFAULT 0.0,
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES countries (id) 
)
'''

sql_students_table = '''
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    first_name VARCHAR(200) NOT NULL,
    last_name VARCHAR(200) NOT NULL,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities (id) 
)
'''


def insert_countries(connection, country):
    try:
        sql = '''INSERT INTO countries
                 (country_title)
                 VALUES (?)
              '''
        cursor = connection.cursor()
        cursor.execute(sql, country)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def insert_cities(connection, city):
    try:
        sql = '''INSERT INTO cities
                 (cities_title, area, country_id)
                 VALUES (?, ?, ?)
              '''
        cursor = connection.cursor()
        cursor.execute(sql, city)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def insert_students(connection, student):
    try:
        sql = '''INSERT INTO students
                 (first_name, last_name, city_id)
                 VALUES (?, ?, ?)
              '''
        cursor = connection.cursor()
        cursor.execute(sql, student)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


my_connection = create_connection("hw.db")
if my_connection:
    print("Connected.")


# create_table(my_connection, sql_countries_table)
# create_table(my_connection, sql_cities_table)
# create_table(my_connection, sql_students_table)

# insert_countries(my_connection, ('Russia',))
# insert_countries(my_connection, ('Kirgizstan',))
# insert_countries(my_connection, ('Japan',))
# insert_cities(my_connection, ('Bishkek', 2561.52, 2))
# insert_cities(my_connection, ('Tokyo', 6322.62, 3))
# insert_cities(my_connection, ('Moscow', 7471.82, 1))
# insert_cities(my_connection, ('Krasnodar', 1727.42, 1))
# insert_cities(my_connection, ('Osh', 5123.41, 2))
# insert_cities(my_connection, ('Tokmok', 9223.73, 2))
# insert_cities(my_connection, ('Osaka', 4723.55, 3))
#
# insert_students(my_connection, ('Anatoly', 'Ivanov', 5))
# insert_students(my_connection, ('Gustavo', 'Fring', 2))
# insert_students(my_connection, ('Sergei', 'Bezrukov', 7))
# insert_students(my_connection, ('Grigory', 'Pavlov', 4))
# insert_students(my_connection, ('Leonid', 'Kamenskiy', 3))
# insert_students(my_connection, ('Nate', 'Diaz', 5))
# insert_students(my_connection, ('Jessy', 'Pinkman', 1))
# insert_students(my_connection, ('Kirill', 'Brivkov', 6))
# insert_students(my_connection, ('Jack', 'Malkovich', 5))
# insert_students(my_connection, ('John', 'Wick', 3))
# insert_students(my_connection, ('Mikhail', 'Petrov', 7))
# insert_students(my_connection, ('John', 'Sina', 2))
# insert_students(my_connection, ('Eldar', 'Jarahov', 1))
# insert_students(my_connection, ('Walter', 'White', 2))
# insert_students(my_connection, ('Homer', 'Simpson', 1))


def get_cities(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, cities_title FROM cities")
        cities = cursor.fetchall()
        return cities
    except sqlite3.Error as e:
        print(e)
        return []


def get_students_by_city(conn, city_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT students.first_name, students.last_name, countries.country_title, cities.cities_title, cities.area FROM students INNER JOIN cities ON students.city_id = cities.id INNER JOIN countries ON cities.country_id = countries.id WHERE cities.id = ?",
            (city_id,))
        students = cursor.fetchall()
        return students
    except sqlite3.Error as e:
        print(e)
        return []


def main():
    conn = sqlite3.connect("hw.db")
    if conn:
        print("Connected to database.")

        cities = get_cities(conn)

        print(
            "Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
        for city in cities:
            print(f"{city[0]}. {city[1]}")

        while True:
            city_id = input("Введите id города: ")
            if city_id == '0':
                break
            city_id = int(city_id)
            students = get_students_by_city(conn, city_id)
            print("\nСписок учеников в выбранном городе:")
            for student in students:
                print(
                    f"Имя: {student[0]}, Фамилия: {student[1]}, Страна: {student[2]}, Город: {student[3]}, Площадь города: {student[4]}")
            print()

        conn.close()
    else:
        print("Failed to connect to database.")


if __name__ == "__main__":
    main()
