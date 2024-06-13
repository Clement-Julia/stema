from django.shortcuts import render

def home(request):
    context = {
        'message': 'Bonjour, monde!'
    }
    return render(request, 'home/home.html', context)

def profile_view(request):
    return render(request, 'user/profil.html')

def handler404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def mentions_legales(request):
    return render(request, 'home/mentions_legales.html')

# def handler500_view(request):
#     return render(request, 'errors/500.html', status=500)