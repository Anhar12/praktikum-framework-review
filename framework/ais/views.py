from django.shortcuts import render

# Create your views here.
def homepage(request):
    context = {
        'home': True,
        'about': False,
    }
    return render(request, 'homepage/index.html', context)

def about(request):
    context = {
        'home': False,
        'about': True,
    }
    return render(request, 'homepage/about.html', context)