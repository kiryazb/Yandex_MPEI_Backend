# Внимание, пременную pk из функции ice_cream_detail
# передавть в шаблон в этом задании не надо.
# Достаточно просто получить ее, как второй обязательный
# аргумент и вызвать соответствующий шаблон
from django.shortcuts import render


def ice_cream_detail(request, pk):
    template_name = 'ice_cream/detail.html'
    return render(request, template_name)


def ice_cream_list(request):
    template_name = 'ice_cream/list.html'
    return render(request, template_name)
