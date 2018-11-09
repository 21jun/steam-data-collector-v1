import schedule
import time
from src.api import ISteamUserStats
import src.api.ISteamApps as SteamApps
import src.utills.GetAppIds as GetAppIds
from src.utills.UrlGenerator import url_generator
from src.crawler import SteamAppParser

# init
cur_players = ISteamUserStats.GetNumberOfCurrentPlayers()
# Loop
schedule.every(5).minutes.do(cur_players.db_update_current_players, cur_players, 'watching_games')
schedule.every(1).hours.do(GetAppIds.db_update_dist_table, 'player_count', 'watching_games')
while True:
    schedule.run_pending()
    time.sleep(10)
