
from django.shortcuts import render

from ice_cream.models import IceCream


def index(request):
    template = 'homepage/index.html'

    ice_cream_list = (
        IceCream.objects
        .filter(is_on_main=True, is_published=True)
        .select_related('wrapper')
        .order_by('title')
    )

    context = {
        'ice_cream_list': ice_cream_list,
    }

    return render(request, template, context)
