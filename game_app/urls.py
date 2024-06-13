# game_app/urls.py

from django.urls import path
from game_app.controllers.GameController import GameController

urlpatterns = [
    path('games/', GameController.display_games, name='games_list'),
    path('games/<int:game_id>/', GameController.display_game_by_id, name='game_detail'),
    path('games/details/<int:game_id>/', GameController.get_game_details, name='get_game_details'),
    path('delete_games/', GameController.delete_games, name='delete_games'),
]
