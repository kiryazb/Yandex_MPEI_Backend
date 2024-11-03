from django.http import HttpResponse

ICE_CREAM = chr(127846)


def ice_cream_detail(request, pk):
    return HttpResponse(f'<h1>{ICE_CREAM}</h1>')


def ice_cream_list(request):
    return HttpResponse(f'<h1>{ICE_CREAM}{ICE_CREAM}{ICE_CREAM}</h1>')