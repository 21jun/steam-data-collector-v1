import requests
import odbc
import src.utills.dateFormatter as df


class GetNumberOfCurrentPlayers:

    def __init__(self):
        connect = odbc.odbc('oasis')
        db = connect.cursor()
        self.db = db

    def __db_get_apps(self, table):
        """
        :param table: Which table you want to use
        :return: app data (appid, name)
        """
        sql = '''SELECT appid, name FROM oasis.''' + str(table)
        self.db.execute(sql)
        r = self.db.fetchall()
        return r

    @staticmethod
    def __api_get_number_of_current_players(appid):
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

    def __db_insert_current_players(self, data):

        sql = '''
            INSERT INTO oasis.current_players(appid, name, player_count, date) VALUES ("%d","%s","%d","%s") '''
        date = df.get_full_date()
        # print(data['appid'], data['name'], data['player_count'], date)
        self.db.execute(sql % (data['appid'], data['name'], int(data['player_count']), date))
        print(data['appid'], data['name'], int(data['player_count']), date)

    def db_update_current_players(self, src='applist'):
        apps = self.__db_get_apps(src)
        for app in apps:
            data = {'appid': app[0], 'name': app[1], 'player_count': self.__api_get_number_of_current_players(app[0])}
            # print(data)
            self.__db_insert_current_players(data)
