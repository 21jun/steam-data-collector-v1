import odbc
import numpy as np
from src.api import ISteamApps
import re


class GetNewAppid:

    def __init__(self):
        connect = odbc.odbc('oasis')
        db = connect.cursor()
        self.db = db

    def __db_get_data_from_src_table(self, col, src_table='applist'):
        sql = 'SELECT ' + str(col) + ' FROM oasis.' + str(src_table)
        self.db.execute(sql)
        data = self.db.fetchall()
        return data

    def __db_delete_duplicated_appid_rows(self):
        sql = """DELETE FROM oasis.watching_games 
                WHERE
                    id NOT IN (SELECT 
                        *
                    FROM
                        (SELECT 
                            MAX(id) AS id
                        FROM
                            oasis.watching_games
                        GROUP BY appid) A)
            """
        self.db.execute(sql)

    def __db_update_dist_table(self, data, dist='watching_games'):
        p = re.compile('[a-zA-z가-힣\s\w]')
        sql_dist = 'INSERT INTO oasis.' + str(dist) + ' (appid, name) VALUES ("%d","%s")'
        for app in data:
            print(app[0], ''.join(p.findall(app[1])))
            self.db.execute(sql_dist % (int(app[0]), ''.join(p.findall(app[1]))))

    def api_update_new_games(self):
        # fetch data
        old_applist_appid = self.__db_get_data_from_src_table('appid', 'applist')
        new_applist = ISteamApps.GetAppList.api_get_app_list()

        # refine data
        old_data_appid = np.array(old_applist_appid).ravel()

        new_data_appid = []
        new_data_name = []
        for app in new_applist:
            new_data_appid.append(app['appid'])
            new_data_name.append(app['name'])
        new_data_appid = np.array(new_data_appid)

        # get new appids
        # setdiff1d(A, B) returns `relative complement` from A to B (order matters)
        new_appids = np.setdiff1d(new_data_appid, old_data_appid)
        print(len(new_appids))

        hash_table = {}
        for d in new_applist:
            hash_table[d['appid']] = d['name']

        result = []
        for app in new_appids:
            # result.append({"appid": app, "name": hash_table[app]})
            result.append((app, hash_table[app]))

        # update watching_games table
        # also delete duplicate rows using group by keyword
        self.__db_update_dist_table(data=result, dist='watching_games')
        self.__db_delete_duplicated_appid_rows()
        # update applist table
        # TODO
