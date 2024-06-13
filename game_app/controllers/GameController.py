# game_app/controllers/GameController.py

import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from game_app.services.ModService import NexusModsService
from game_app.services.GameService import GameService
from game_app.models import GameLibrary

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
        filter_library = request.GET.get('filter_library') == 'on'

        request.session['search_query'] = search_query
        request.session['filter_library'] = filter_library

        if search_query:
            filtered_games = [game for game in games if search_query in game['name'].strip().lower()]
        else:
            filtered_games = games

        # Filtre des jeux de l'user
        if request.user.is_authenticated and filter_library:
            user_game_ids = GameLibrary.objects.filter(user=request.user).values_list('game_id', flat=True)
            filtered_games = [game for game in filtered_games if game['appid'] in user_game_ids]

        page = request.GET.get('page', 1)
        paginator = Paginator(filtered_games, 25)  # 25 jeux par page

        try:
            games_page = paginator.page(page)
        except PageNotAnInteger:
            games_page = paginator.page(1)
        except EmptyPage:
            games_page = paginator.page(paginator.num_pages)
        
        game_ids = [game['appid'] for game in games_page]
        header_images = GameService.get_games_images_parallel(game_ids)

        for game, header_image in zip(games_page, header_images):
            game['header_image'] = header_image

        return render(request, 'game_app/gamesDisplay.html', {
            'games': games_page,
            'page': page,
            'filter_library': filter_library,
            'search_query': search_query
        })
    
    @staticmethod
    def display_game_by_id(request, game_id):
        game = GameService.get_game_details(game_id)
        game_in_library = False
        if request.user.is_authenticated:
            game_in_library = GameLibrary.objects.filter(user=request.user, game_id=game_id).exists()
        
        page = request.GET.get('page', 1)
        search_query = request.session.get('search_query', '')
        filter_library = request.session.get('filter_library', False)

        game['appid'] = game_id
        mods = NexusModsService.fetch_mods(game['name'])
        return render(request, 'game_app/gameDetail.html', {
            'game': game,
            'mods': mods,
            'page': page,
            'search_query': search_query,
            'filter_library': filter_library,
            'game_in_library': game_in_library
        })
        
    @staticmethod
    def get_game_details(request, game_id):
        game = GameService.get_game_details(game_id)
        return JsonResponse(game)

    # Pour du debugging, supprime var cache/session
    @staticmethod
    def delete_games(request):
        if 'games' in request.session:
            del request.session['games']
        return JsonResponse({'status': 'success'})

    @staticmethod
    @login_required
    def add_game_to_library(request, game_id):
        game_name = request.POST.get('game_name')
        game, created = GameLibrary.objects.get_or_create(user=request.user, game_id=game_id, defaults={'game_name': game_name})
        if created:
            return HttpResponseRedirect(reverse('game_detail', args=[game_id]))
        return HttpResponseRedirect(reverse('game_detail', args=[game_id]) + '?already_in_library=true')
    
    @staticmethod
    @login_required
    def remove_game_from_library(request, game_id):
        game = get_object_or_404(GameLibrary, user=request.user, game_id=game_id)
        game.delete()
        return HttpResponseRedirect(reverse('game_detail', args=[game_id]))