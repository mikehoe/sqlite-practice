import sqlite3

if __name__ == '__main__':
    print('sqlite test')

    connection = sqlite3.connect("practice.db")

    try:
        with connection:
            connection.execute(
                """
                """
            )
    finally:
        connection.close()
