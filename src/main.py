import src.api.ISteamUserStats as SteamUserStats
import src.api.ISteamApps as SteamApps
import src.utills.GetAppIds as GetApp

# SteamApps.db_update_app_list()
SteamUserStats.db_update_current_players('watching_games')
# GetApp.db_update_dist_table('player_count', 'watching_games')
