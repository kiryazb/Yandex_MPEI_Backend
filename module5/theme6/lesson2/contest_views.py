from django.shortcuts import render

from .forms import ContestForm



def proposal_create(request):
    form = ContestForm()
    context = {'form': form}
    return render(request, 'contest/form.html', context)


def accepted(request):
    return render(request, 'contest/proposal_accepted.html')
