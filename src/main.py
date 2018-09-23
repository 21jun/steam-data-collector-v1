from src.api import ISteamUserStats
import src.api.ISteamApps as SteamApps
import src.utills.GetAppIds as GetAppIds
from src.utills.UrlGenerator import url_generator
from src.crawler import SteamAppParser

GetAppIds.db_update_dist_table('player_count', 'watching_games')