# game_app/services/GameService.py

import requests
from bs4 import BeautifulSoup

class GameService:
    STEAM_CHARTS_URL = "https://steamcharts.com/top/p.{}"
    STORE_URL = "https://store.steampowered.com/api/appdetails?appids={}"

    @staticmethod
    def get_top_played_games():
        games = []
        for page in range(1, 8):  # Pages 1 to 8
            url = GameService.STEAM_CHARTS_URL.format(page)
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.select('table.common-table tbody tr')
                for row in rows:
                    link = row.select_one('td:nth-child(2) a')
                    name = link.text.strip()
                    href = link['href']
                    appid = href.split('/')[-1]  # Extraire l'ID Steam à partir de l'URL
                    current_players = row.select_one('td:nth-child(3)').text.strip()
                    games.append({
                        'name': name,
                        'appid': appid,
                        'current_players': current_players
                    })
        return games

    @staticmethod
    def get_game_details(appid):
        endpoint = GameService.STORE_URL.format(appid)
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json().get(str(appid), {}).get('data', {})
            if data:
                return {
                    'name': data.get('name'),
                    'short_description': data.get('short_description'),
                    'release_date': data.get('release_date', {}).get('date'),
                    'developers': data.get('developers', []),
                    'publishers': data.get('publishers', []),
                    'price_overview': data.get('price_overview', {}).get('final_formatted', "Free"),
                    'header_image': data.get('header_image')  # URL de l'image de couverture
                }
        return {}

    @staticmethod
    def get_game_by_id(game_id):
        return GameService.get_game_details(game_id)