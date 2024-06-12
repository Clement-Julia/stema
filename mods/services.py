import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

NEXUSMODS_API_URL = 'https://api.nexusmods.com/v1/'

class NexusModsService:
    @staticmethod
    def fetch_mods(game_domain_name):
        headers = {
            'apikey': os.environ.get('NEXUSMODS_API_KEY'),
            'Accept': 'application/json'
        }
        response = requests.get(f'{NEXUSMODS_API_URL}games/{game_domain_name}/mods/trending.json', headers=headers)

        if response.status_code == 200:
            mods_data = response.json()
            for mod in mods_data:
                if 'description' in mod:
                    mod['description'] = NexusModsService.clean_html(mod['description'])
                if 'created_time' in mod:
                    mod['created_time'] = datetime.fromisoformat(mod['created_time'])
            return mods_data
        else:
            print(f"Failed to fetch mods: {response.status_code}")
            return []
        
    @staticmethod
    def fetch_files(game_domain_name, mod_id):
        headers = {
            'apikey': os.environ.get('NEXUSMODS_API_KEY'),
            'Accept': 'application/json'
        }
        response = requests.get(f'{NEXUSMODS_API_URL}games/{game_domain_name}/mods/{mod_id}/files.json', headers=headers)

        if response.status_code == 200:
            files_data = response.json()
            # for mod in files_data:
            #     if 'description' in mod:
            #         mod['description'] = NexusModsService.clean_html(mod['description'])
            #     if 'created_time' in mod:
            #         mod['created_time'] = datetime.fromisoformat(mod['created_time'])
            return files_data
        else:
            print(f"Failed to fetch mods: {response.status_code}")
            return []
        
    def clean_html(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        return soup.prettify()