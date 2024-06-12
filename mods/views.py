from django.shortcuts import render
from django.http import JsonResponse  # Import JsonResponse
from .services import NexusModsService

def mod_list(request):
    game_domain_name = "skyrim"
    mods = NexusModsService.fetch_mods(game_domain_name)
    return render(request, 'mods/mod_list.html', {'mods': mods})

def view_mods(request, game_domain_name):
    mods = NexusModsService.fetch_mods(game_domain_name)
    return render(request, 'mods/mod_list.html', {'mods': mods})

def get_files(request, game_domain_name, mod_id):
    files = NexusModsService.fetch_files(game_domain_name, mod_id)
    
    return JsonResponse(files)