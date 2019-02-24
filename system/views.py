from django.shortcuts import render


# Create your views here.
def about_page(request):
    context = {
    }
    return render(request, 'about.html', context)


def add_tag_page(request):
    context = {
    }
    return render(request, 'add_tag.html', context)
