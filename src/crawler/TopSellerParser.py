import requests
from bs4 import BeautifulSoup
import threading
from src.modules.DateFormatter import date_pass
from src.modules.DataBaseConnector import DataBaseConnector
import time
from tqdm import tqdm


class TS_DataBase_Conn(DataBaseConnector):

    def __init__(self):
        super().__init__()
        self.date = date_pass()
        self.repeat = 0

    def run(self):
        self.date = date_pass()
        self.repeat = 0

        self.__db_


    def __db_insert_data(self, games):
        sql = '''INSERT INTO oasis.games(title, ranking, price, price_discounted, date, release_date, type, id_title, 
        id_num) VALUES ("%s","%d","%d","%d","%s","%s","%s","%s","%s") '''

        for i in tqdm(range(0, 1000)):
            print(games[i]['title'])
            try:
                self.db.execute(sql % (
                    games[i]['title'], games[i]['rank'], games[i]['price'], games[i]['price_discounted'],
                    games[i]['date'],
                    games[i]['release'], games[i]['type'], games[i]['id_title'], games[i]['id_num']))
            except:
                print("UNICODE ERROR")
                self.db.execute(sql % (
                    "NONE", games[i]['rank'], games[i]['price'], games[i]['price_discounted'], games[i]['date'],
                    games[i]['release'], games[i]['type'], games[i]['id_title'], games[i]['id_num']))


TDC = TS_DataBase_Conn()
