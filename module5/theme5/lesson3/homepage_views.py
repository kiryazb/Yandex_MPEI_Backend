
from django.shortcuts import render

from ice_cream.models import IceCream


def index(request):
    template = 'homepage/index.html'
    # Добавьте фильтрацию по полю is_published.
    ice_cream_list = IceCream.objects.values(
        'id', 'title', 'description'
    ).filter(is_published=True)
    context = {
        'ice_cream_list': ice_cream_list,
    }

    return render(request, template, context)
