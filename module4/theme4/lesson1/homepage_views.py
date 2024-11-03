from django.shortcuts import render


def index(request):
    template_name = 'homepage/index.html'
    return render(request, template_name)
