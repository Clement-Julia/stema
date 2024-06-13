# game_app/services/GameService.py

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache

class GameService:
    STEAM_CHARTS_URL = "https://steamcharts.com/top/p.{}"
    STORE_URL = "https://store.steampowered.com/api/appdetails?appids={}"

    @staticmethod
    def get_top_played_games():
        games = []
         # Pages 1 à 8 de steamcharts pour un total de 200 jeux
        for page in range(1, 8):
            url = GameService.STEAM_CHARTS_URL.format(page)
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.select('table.common-table tbody tr')
                for row in rows:
                    link = row.select_one('td:nth-child(2) a')
                    name = link.text.strip()
                    href = link['href']
                    # Extraire l'ID Steam à partir de l'URL
                    appid = href.split('/')[-1] 
                    players = row.select_one('td:nth-child(3)').text.strip()
                    games.append({
                        'name': name,
                        'appid': appid,
                        'players': players
                    })
        return games

    @staticmethod
    def get_game_details(appid):
        cache_key = f'game_details_{appid}'
        game_details = cache.get(cache_key)

        if not game_details:
            endpoint = GameService.STORE_URL.format(appid)
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json().get(str(appid), {}).get('data', {})
                if data:
                    print(GameService.get_metacritic_color(data.get('metacritic', {}).get('score')))
                    game_details = {
                        'name': data.get('name'),
                        'short_description': data.get('short_description'),
                        'release_date': data.get('release_date', {}).get('date'),
                        'developers': data.get('developers', []),
                        'publishers': data.get('publishers', []),
                        'price_overview': data.get('price_overview', {}).get('final_formatted', "Free"),
                        'header_image': data.get('header_image'),
                        'detailed_description': data.get('detailed_description', ''),
                        'platforms': data.get('platforms', {}),
                        'screenshots': data.get('screenshots', []),
                        'metacritic_score': data.get('metacritic', {}).get('score'),
                        'metacritic_url': data.get('metacritic', {}).get('url'),
                        'metacritic_color': GameService.get_metacritic_color(data.get('metacritic', {}).get('score')),
                        'genres': [genre['description'] for genre in data.get('genres', [])]
                    }
                    cache.set(cache_key, game_details, timeout=60*60)  # Cache for 1 hour
                else:
                    game_details = {}
            else:
                game_details = {}
        return game_details

    @staticmethod
    def get_game_image(appid):
        cache_key = f'get_game_image{appid}'
        header_image = cache.get(cache_key)

        if not header_image:
            endpoint = GameService.STORE_URL.format(appid)
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json().get(str(appid), {}).get('data', {})
                if data:
                    header_image = data.get('header_image')
                    cache.set(cache_key, header_image, timeout=60*60)
            else:
                header_image = None
            
        return header_image
    
    @staticmethod
    def get_games_details_parallel(game_ids):
        with ThreadPoolExecutor(max_workers=10) as executor:
            details = list(executor.map(GameService.get_game_details, game_ids))
        return details
    
    @staticmethod
    def get_games_images_parallel(game_ids):
        with ThreadPoolExecutor(max_workers=10) as executor:
            header_images = list(executor.map(GameService.get_game_image, game_ids))
        return header_images
    
    @staticmethod
    def get_metacritic_color(score):
        if score is not None:
            if score >= 65:
                return "green"
            elif 45 <= score < 65:
                return "yellow"
            else:
                return "red"
        return "green" 