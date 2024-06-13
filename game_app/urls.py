# game_app/urls.py

from django.urls import path
from game_app.controllers.GameController import GameController
from game_app.services.Proxy import proxy_view

urlpatterns = [
    path('games/', GameController.display_games, name='games_list'),
    path('games/<int:game_id>/', GameController.display_game_by_id, name='game_detail'),
    path('games/details/<int:game_id>/', GameController.get_game_details, name='get_game_details'),
    path('delete_games/', GameController.delete_games, name='delete_games'),
    path('add_game_to_library/<int:game_id>/', GameController.add_game_to_library, name='add_game_to_library'),
    path('remove_game_from_library/<int:game_id>/', GameController.remove_game_from_library, name='remove_game_from_library'),
    path('mods/proxy/', proxy_view, name='proxy'),
]
