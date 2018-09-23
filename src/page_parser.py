from src.utills.UrlGenerator import url_generator
from src.crawler import SteamAppParser


def page_parser(data_base, table, crawler):
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
for i in range(100):
    page_parser(data_base, 'watching_games', crawler)

del crawler
