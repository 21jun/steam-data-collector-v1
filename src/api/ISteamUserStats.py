import requests
import odbc
import src.utills.dateFormatter as df


def db_get_all_apps():
    """
    :return: all apps(appid, name)
    """
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    sql = '''SELECT appid, name FROM oasis.applist'''
    db.execute(sql)
    r = db.fetchall()
    return r


def db_get_apps(table):
    """
    :param table: Which table you want to use
    :return: app data (appid, name)
    """
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    sql = '''SELECT appid, name FROM oasis.appid'''
    db.execute(sql)
    r = db.fetchall()
    return r


def api_get_number_of_current_players(appid):
    """
    return current players of the game(appid)
    :param appid: appid for game
    :return: number of current players
    """
    url = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v0001/?appid=' \
          + str(appid) + '&format=json'
    req = requests.get(url)
    json_data = req.json()
    try:
        player_count = json_data['response']['player_count']
        # print(player_count)
        return player_count
    except KeyError:
        return 0
    except:
        return 0


def db_insert_current_players(data):
    connect = odbc.odbc('oasis')
    db = connect.cursor()
    sql = '''
        INSERT INTO oasis.cur_players(appid, name, player_count, date) VALUES ("%d","%s","%d","%s") '''
    date = df.get_full_date()
    print(data['appid'], data['name'], data['player_count'], date)
    db.execute(sql % (data['appid'], data['name'], int(data['player_count']), date))


def db_update_current_players():
    apps = db_get_all_apps()
    for app in apps:
        data = {'appid': app[0], 'name': app[1], 'player_count': api_get_number_of_current_players(app[0])}
        # print(data)
        db_insert_current_players(data)
