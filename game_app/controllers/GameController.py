# game_app/controllers/GameController.py

import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from game_app.services.ModService import NexusModsService
from game_app.services.GameService import GameService

class GameController:
    
    @staticmethod
    def home(request):
        return redirect('games_list')
    
    @staticmethod
    def display_games(request):
        if 'games' not in request.session:
            games = GameService.get_top_played_games()
            request.session['games'] = games
        else:
            games = request.session['games']

        search_query = request.GET.get('search', '').strip().lower()
        if search_query:
            filtered_games = [game for game in games if search_query in game['name'].strip().lower()]
        else:
            filtered_games = games
        
        page = request.GET.get('page', 1)
        paginator = Paginator(filtered_games, 25)  # 25 jeux par page

        try:
            games_page = paginator.page(page)
        except PageNotAnInteger:
            games_page = paginator.page(1)
        except EmptyPage:
            games_page = paginator.page(paginator.num_pages)
        
        # Récupérer les images pour les jeux paginés en parallèle
        game_ids = [game['appid'] for game in games_page]
        header_images = GameService.get_games_images_parallel(game_ids)

        for game, header_image in zip(games_page, header_images):
            game['header_image'] = header_image

        return render(request, 'game_app/gamesDisplay.html', {
            'games': games_page,
            'page': page
        })
    
    @staticmethod
    def display_game_by_id(request, game_id):
        game = GameService.get_game_details(game_id)
        mods = NexusModsService.fetch_mods(game['name'])
        page = request.GET.get('page', 1)
        return render(request, 'game_app/gameDetail.html', {'game': game, 'mods': mods, 'page': page})

    @staticmethod
    def get_game_details(request, game_id):
        game = GameService.get_game_details(game_id)
        return JsonResponse(game)

    @staticmethod
    def delete_games(request):
        if 'games' in request.session:
            del request.session['games']
        return JsonResponse({'status': 'success'})
