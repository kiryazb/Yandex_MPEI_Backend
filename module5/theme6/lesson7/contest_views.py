from django.shortcuts import render

from .forms import ContestForm
from .models import Contest


def proposal(request):
    form = ContestForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'contest/form.html', {'form': form})


def proposal_list(request):
    recipes = Contest.objects.all().order_by('id')
    return render(request, 'contest/contest_list.html', {'recipes': recipes})
