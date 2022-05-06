from django.db import connection



def query_all( sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row))for row in cursor.fetchall()]

def query_one( sql, params=None):
    with connection.cursor() as cursor:
        print(sql)
        cursor.execute(sql, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row))for row in cursor.fetchone()]
