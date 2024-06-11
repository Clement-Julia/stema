# game_app/controllers/GameController.py

import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import redirect, render
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
        
        page = request.GET.get('page', 1)
        # 25 jeux par page
        paginator = Paginator(games, 25)

        try:
            games_page = paginator.page(page)
        except PageNotAnInteger:
            games_page = paginator.page(1)
        except EmptyPage:
            games_page = paginator.page(paginator.num_pages)
        
        # Récupérer les détails pour les jeux paginés en parallèle
        game_ids = [game['appid'] for game in games_page]
        game_details = GameService.get_games_details_parallel(game_ids)

        for game, details in zip(games_page, game_details):
            game['header_image'] = details.get('header_image')

        games_json = json.dumps(list(games_page), default=str)

        return render(request, 'game_app/gamesDisplay.html', {
            'games': games_page,
            'games_json': games_json
        })
    
    @staticmethod
    def display_game_by_id(request, game_id):
        game = GameService.get_game_by_id(game_id)
        return render(request, 'game_app/gameDetail.html', {'game': game})

    @staticmethod
    def get_game_details(request, game_id):
        game = GameService.get_game_by_id(game_id)
        return JsonResponse(game)

    @staticmethod
    def delete_games(request):
        if 'games' in request.session:
            del request.session['games']
        return JsonResponse({'status': 'success'})
