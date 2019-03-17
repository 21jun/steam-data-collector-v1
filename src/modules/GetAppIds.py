import odbc

'''
How to use:
1. dist table will be truncated
2. 
'''


def __db_get_data_from_src_table(sql):
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    db.execute(sql)
    r = db.fetchall()
    return r


def db_update_dist_table(src, dist):
    sql_src = 'select max(id_num), title from oasis.' + str(src) + ' group by title'
    data = __db_get_data_from_src_table(sql_src)
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    db.execute('TRUNCATE oasis.' + str(dist))
    sql_dist = 'INSERT INTO oasis.' + str(dist) + ' (appid, name) VALUES ("%d","%s")'
    i = 0
    for app in data:
        print(app[0], app[1])
        i = i + 1
        db.execute(sql_dist % (int(app[0]), app[1]))
    print(i)
