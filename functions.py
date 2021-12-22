import psycopg2


def check_configs():
    pass


def select_all(table, current_connection):
    local_cursor = current_connection.cursor()

    local_cursor.execute(
        """SELECT * from """ + table + """ 
        ORDER BY name"""
    )

    return local_cursor.fetchall()


def select_all_titles(current_connection):
    local_cursor = current_connection.cursor()

    local_cursor.execute(
        """SELECT tit.id, tit.name, pub.name
        FROM titles tit
        INNER JOIN publishers pub ON tit.publisher_id = pub.id
        ORDER BY tit.name"""
    )

    return local_cursor.fetchall()


def select_volumes(title_name, current_connection):
    local_cursor = current_connection.cursor()

    local_cursor.execute(
        """SELECT vol.id, vol.name, vol.year, pub.name, per.name, per2.name
        FROM (((((volumes vol
        INNER JOIN titles tit ON vol.title_id = tit.id)
        INNER JOIN publishers pub ON tit.publisher_id = pub.id)
        INNER JOIN posts pos ON (vol.id = pos.volume_id AND pos.profession_id = 1))
        INNER JOIN posts pos2 ON (vol.id = pos2.volume_id AND pos2.profession_id = 2))
        INNER JOIN persons per ON pos.person_id = per.id)
        INNER JOIN persons per2 ON pos2.person_id = per2.id
        WHERE tit.name like '""" + title_name + """' 
        ORDER BY vol.year"""
    )

    return local_cursor.fetchall()


def select_publisher(publisher_name, current_connection):
    local_cursor = current_connection.cursor()

    local_cursor.execute(
        """SELECT tit.id, tit.name, vol.year
        FROM titles tit, publishers pub, volumes vol
        where pub.name like '""" + publisher_name + """' and tit.publisher_id = pub.id and vol.title_id = tit.id
        and vol.number = 1 
        ORDER BY name"""
    )

    return local_cursor.fetchall()


def select_author(person_name, current_connection):
    local_cursor = current_connection.cursor()

    local_cursor.execute(
        """SELECT vol.year, vol.name, tit.name, pub.name, prof.name
        FROM ((((posts
        INNER JOIN persons ON persons.id = posts.person_id)
        INNER JOIN volumes vol ON vol.id = posts.volume_id)
        INNER JOIN professions prof ON prof.id = posts.profession_id)
        INNER JOIN titles tit ON tit.id = vol.title_id)
        INNER JOIN publishers pub ON pub.id = tit.publisher_id
        WHERE persons.name like '""" + person_name + """'
        ORDER BY vol.year"""
    )

    return local_cursor.fetchall()


def select_decades(decade, current_connection):
    local_cursor = current_connection.cursor()

    local_cursor.execute(
        """SELECT vol.id, vol.year, vol.name,  vol.number, tit.name, pub.name
        FROM (volumes vol
        INNER JOIN titles tit ON vol.title_id = tit.id)
        INNER JOIN publishers pub ON tit.publisher_id = pub.id
        WHERE vol.year BETWEEN """ + str(decade) + """ AND """ + str(int(decade) + int(10)) + """
        ORDER BY year"""
    )

    return local_cursor.fetchall()


def connect_to_db(ip, user_name, user_password, db_name, port="5432"):
    try:
        new_connection = psycopg2.connect(
            user=user_name, password=user_password, host=ip, database=db_name, port=port
        )

        return new_connection
    except:
        return False
