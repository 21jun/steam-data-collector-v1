import requests
import odbc


def api_get_app_list():
    """
    return all games in steam
    approximately 66000+
    :return: list of {"appid":"appid (number)" , "name":"name of game"}
    """
    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0001/'
    req = requests.get(url)
    json_data = req.json()
    # print(json_data)
    applist = json_data['applist']['apps']['app']
    return applist


def db_insert_appid(sql, data):
    """
    TODO: prevent sql injection
    insert data into db
    :param sql: sql query
    :param data: data
    :return: success or fail
    """
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    for app in data:
        appid = int(app['appid'])
        name = app['name'].replace('\"', "'")
        db.execute(sql % (appid, name))
        print(app)


def db_clear_old_appid():
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    sql = '''TRUNCATE oasis.appid'''
    db.execute(sql)


def db_update_app_list():
    data = api_get_app_list()
    db_clear_old_appid()
    sql = '''
        INSERT INTO oasis.appid(appid, name) 
        VALUES ("%d",("%s")) '''

    db_insert_appid(sql, data)



