from django.shortcuts import render

# def simulate_error(request):
#     # Simuler une erreur en levant une exception
#     raise Exception("Ceci est une erreur 500 provoquée")

def home(request):
    # Logique de traitement de la requête ici
    context = {
        'message': 'Bonjour, monde!'
    }
    return render(request, 'home/home.html', context)

def profile_view(request):
    # Logique de traitement de la requête pour afficher le profil
    return render(request, 'user/profil.html')

def handler404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500_view(request):
    return render(request, 'errors/500.html', status=500)
