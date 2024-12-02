from django.shortcuts import render

ice_cream_catalog = [
    {
        'id': 0,
        'title': 'Классический пломбир',
        'description': 'Настоящее мороженое, '
                       'для истинных ценителей вкуса. '
                       'Если на столе появляется пломбир'
                       ' — это не надолго.',
    },
    {
        'id': 1,
        'title': 'Мороженое с кузнечиками',
        'description': 'В колумбийском стиле: мороженое '
                       'с добавлением настоящих карамелизованных кузнечиков.',
    },
    {
        'id': 2,
        'title': 'Мороженое со вкусом сыра чеддер',
        'description': 'Вкус настоящего сыра в вафельном стаканчике.',
    },
]


def ice_cream_detail(request, pk):
    template = 'ice_cream/detail.html'

    return render(request, template, {'ice_cream': ice_cream_catalog[pk]})


def ice_cream_list(request):
    template = 'ice_cream/list.html'
    return render(request, template)