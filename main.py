import psycopg2
from psycopg2 import Error

import Frames
from config import *


try:
    # connect
    # connection = psycopg2.connect(
    #     user="postgres", password="qwerty1245", host="192.168.56.1", port="5432", database="comicsDB"
    # )
    connection = psycopg2.connect(
        user=user, password=password, host=host, database=db_name
    )

    # cursor
    cursor = connection.cursor()

    cursor.execute(
        "SELECT version();"
    )

    print(f"Server version: {cursor.fetchone()}\n")

    cursor.execute(
        """SELECT * from publishers"""
    )
    print(cursor.fetchall()[0][1])

    Frames.choose_window("connect")

    # print(select_all("countries"))
    # print(select_all("persons"))
    # print(select_all("publishers"))
    # print(select_all("titles"))
    # print(select_all("volumes"))
    # print(select_all("professions"))
    # print(select_all("posts"))

except (Exception, Error) as _ex:
    print("[ERROR] Error while working with PostgreSQL", _ex)
finally:
    if 'connection' in locals():
        cursor.close()
        connection.close()
        print("\n\n[INFO] PostgreSQL connection closed")
