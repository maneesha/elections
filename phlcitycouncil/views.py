from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader
from .models import Person, District, Election, Candidate, Vote

from django.db.models import Count, Sum

# Create your views here.

def index(request):
    # Return some ordinary text
    # return HttpResponse("Hello, main page.")

    sum_votes = Vote.objects.all().values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name').annotate(Sum('vote_count'))

    # return HttpResponse(sum_votes)

    # elections_list = Election.objects.all().order_by("district__ward")
    # template = loader.get_template('phlcitycouncil/index.html')
    context = {
        "sum_votes":sum_votes,
    }
    # output =  ", ".join([q.district.ward + q.district.division + str(q.election_date) + q.office.office for q in elections])

    # return render(request, 'phlcitycouncil/index.html', context)
    return render(request, 'phlcitycouncil/index.html', context)


def phlcitycouncil(request):
    return HttpResponse("vistiing phlcitycouncil")

def about(request):
    return HttpResponse('the about page')