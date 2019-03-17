from src.api import ISteamUserStats
from src.api import ISteamApps
from src.modules import GetNewGames
import schedule
from time import sleep

if __name__ == "__main__":
    # init (instance)
    cur_players = ISteamUserStats.GetNumberOfCurrentPlayers()
    app_list = ISteamApps.GetAppList()
    new_games = GetNewGames.GetNewAppid()

    # task1 : update watching_games table every day
    schedule.every().day.at("12:00").do(new_games.api_update_new_games)

    # task2 : get current_players of watching_games
    schedule.every().hour.do(cur_players.db_update_current_players, cur_players, 0, 'watching_games',
                             'app_current_players2')

    # scheduler loop
    while True:
        schedule.run_pending()
        sleep(0.5)
