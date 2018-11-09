from src.utills.UrlGenerator import url_generator
from src.crawler import SteamAppParser
import src.utills.GetAppIds as GetAppIds
import schedule
import time


def page_parser(data_base, table, crawler):
    GetAppIds.db_update_dist_table('player_count', 'watching_games')
    apps = data_base.db_get_apps(table)
    for app in apps:
        info = {
            'appid': int(app[0]),
            'name': app[1]
        }
        try:
            soup = crawler.parse_url(url_generator(info['appid']))
            result = SteamAppParser.GetAppInfo(soup, info).get_info()
            print(result)
            data_base.db_update_app_data(result)
        except TimeoutError:
            print("TIME OUT")


# initialize
crawler = SteamAppParser.HeadlessChrome('C:/chromedriver_win32/chromedriver')
data_base = SteamAppParser.DataBaseConnector()

page_parser(data_base, 'watching_games', crawler)
del crawler
# while True:
#     page_parser(data_base, 'watching_games', crawler)
#     time.sleep(4*60*60)

# del crawler
