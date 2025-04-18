import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='Gulnara07041986',
        host='localhost'
    )
    print("Успешное подключение!")
    conn.close()
except Exception as e:
    print(f"Ошибка: {e}")