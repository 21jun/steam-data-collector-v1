from src.api import ISteamUserStats
import src.api.ISteamApps as SteamApps
import src.utills.GetAppIds as GetApp
from src.crawler import SteamAppParser

crawler = SteamAppParser.HeadlessChrome('C:/chromedriver_win32/chromedriver')
soup = crawler.parse_url('https://store.steampowered.com/app/381210/Dead_by_Daylight/')
# soup = crawler.parse_url('https://store.steampowered.com/app/579490/RUSH_A_Disney__PIXAR_Adventure/')
info = {
    'appid': 381210,
    'title': 'Dead by Daylight'
}


i = SteamAppParser.GetAppInfo(soup, info)
i.get_recent_review()
# applist = SteamApps.GetAppList()
# applist.db_update_app_list()
# cur_players = ISteamUserStats.GetNumberOfCurrentPlayers()
# cur_players.db_update_current_players()
# GetApp.db_update_dist_table('player_count', 'watching_games')
