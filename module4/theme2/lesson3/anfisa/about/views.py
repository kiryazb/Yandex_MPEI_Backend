from django.http import HttpResponse


def description(request):
    return HttpResponse('<h1>Урра, заработало!</h1>')