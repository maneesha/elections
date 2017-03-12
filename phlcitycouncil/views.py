from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader
from .models import Person, District, Election, Candidate, Vote

from django.db.models import Count, Sum

# Create your views here.

def index(request):
    return render(request, 'phlcitycouncil/index.html')


def vote_count(request):
    # PROBLEM:  THIS DOES NOT SEPARATE BY ELECTION.  VIEW to HTML TEMPLATE vote_count.html SUMS UP ALL VOTES NOT JUST ONE ELECTION


    sum_votes_by_candidate = Vote.objects.all().values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes')

    # Retrieve At Large Republican candidates and votes
    sum_votes_by_candidate_atlarge_dems = Vote.objects.filter(election__office__office='COUNCIL AT LARGE', candidate__party="Democrat").values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes')

    # Retrive At Large Democrate candidates and votes
    sum_votes_by_candidate_atlarge_reps = Vote.objects.filter(election__office__office='COUNCIL AT LARGE', candidate__party="Republican").values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes')

    # Retrieve At Large Other Party candidates and votes
    sum_votes_by_candidate_atlarge_other = ""

    sum_votes_by_candidate_district = Vote.objects.filter(election__office__office__startswith='DIST').values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes')



    sum_votes_by_office = Vote.objects.all().values('election__office__office').annotate(Sum('vote_count'))

    sum_votes_by_office_district = Vote.objects.filter(election__office__office__startswith='DIST').values('election__office__office').annotate(Sum('vote_count'))


    sum_votes_by_candidate_atlarge_other = Vote.objects.filter(election__office__office='COUNCIL AT LARGE').values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes').exclude(candidate__party__in=["Democrat", "Republican"])


    context = {
        "sum_votes_by_candidate":sum_votes_by_candidate,
        "sum_votes_by_office":sum_votes_by_office,
        "sum_votes_by_candidate_atlarge_dems":sum_votes_by_candidate_atlarge_dems,
        "sum_votes_by_candidate_atlarge_reps":sum_votes_by_candidate_atlarge_reps,
        "sum_votes_by_candidate_atlarge_other":sum_votes_by_candidate_atlarge_other,
        "sum_votes_by_candidate_district":sum_votes_by_candidate_district,
        "sum_votes_by_office_district":sum_votes_by_office_district,
        "sum_votes_by_candidate_atlarge_other": sum_votes_by_candidate_atlarge_other


    }

    return render(request, 'phlcitycouncil/vote_count.html', context)


def phlcitycouncil(request):
    return HttpResponse("vistiing phlcitycouncil")

def about(request):
    return HttpResponse('the about page')