import requests
import odbc
import time
from json import JSONDecodeError
import src.utills.dateFormatter as dF
from datetime import datetime


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
        try:
            req = requests.get(url)
        except ConnectionError:
            return None
        except TimeoutError:
            return None
        except:
            print("Error occur")
            return None

        try:
            json_data = req.json()
        except JSONDecodeError:
            return None

        try:
            player_count = json_data['response']['player_count']
            # print(player_count)
            return player_count
        except KeyError:
            return None
        except:
            return None

    def __db_insert_current_players(self, data, target):

        sql = 'INSERT INTO oasis.' + str(target) + '''(appid, name, player_count, date) 
        VALUES ("%d","%s","%d","%s") '''
        date = dF.get_full_date()
        # print(data['appid'], data['name'], data['player_count'], date)
        if not data['player_count']:
            print("API ERROR")
            print(data['appid'], data['name'], data['player_count'], date)
            return
        self.db.execute(sql % (data['appid'], data['name'], int(data['player_count']), date))
        print(data['appid'], data['name'], int(data['player_count']), date)

    @staticmethod
    def db_update_current_players(self, delay_sec=0, src='applist', target='app_current_players'):
        apps = self.__db_get_apps(src)
        for idx, app in enumerate(apps):
            # time.sleep(delay_sec)
            data = {'appid': app[0], 'name': app[1], 'player_count': self.__api_get_number_of_current_players(app[0])}
            if not data['player_count']:
                print("api error")
                # continue
            print(str(datetime.now()), data, str(idx) + "/" + str(len(apps)))
            self.__db_insert_current_players(data, target)
        print("====================" + str(datetime.now()) + "====================")
