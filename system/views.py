from django.shortcuts import render


# Create your views here.
def landing_page(request):
    context = {
    }
    return render(request, 'landing.html', context)



def legal_page(request):
    context = {
    }
    return render(request, 'legal.html', context)

