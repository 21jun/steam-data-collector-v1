import odbc


def db_get_data_from_src_table(sql):
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    db.execute(sql)
    r = db.fetchall()
    return r


def db_update_dist_table(src, dist):
    sql_src = 'select max(id_num), title from oasis.' + str(src) + ' group by title'
    data = db_get_data_from_src_table(sql_src)

    connect = odbc.odbc('oasis')
    db = connect.cursor()
    sql_dist = 'INSERT INTO oasis.' + str(dist) + ' (appid, name) VALUES ("%d","%s")'
    for app in data:
        db.execute(sql_dist % (int(app[0]), app[1]))
