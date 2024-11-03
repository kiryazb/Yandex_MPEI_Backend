from django.http import HttpResponse


def ice_cream_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}')


def ice_cream_list(request):
    return HttpResponse('Каталог мороженого')