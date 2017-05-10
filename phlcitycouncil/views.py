from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader
from .models import Person, District, Election, Candidate, Vote

from django.db.models import Count, Sum

# Create your views here.

def index(request):
    return render(request, 'phlcitycouncil/index.html')


def vote_count(request, election_year):
    # PROBLEM:  THIS DOES NOT SEPARATE BY ELECTION.  VIEW to HTML TEMPLATE vote_count.html SUMS UP ALL VOTES NOT JUST ONE ELECTION

    # not being used?
    # sum_votes_by_candidate = Vote.objects.all().values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes')

    elections = {'2011': '2011-11-08', '2015': '2015-11-03'}

    try:

        current_election = Vote.objects.filter(election__election_date = elections[election_year])
        print("ELECTION YEAR: ", election_year)
        print("TYPE: ", type(election_year))
        print("FROM DICT: ", elections[election_year])

        # Retrieve At Large Democrat candidates and votes
        sum_votes_by_candidate_atlarge_dems = current_election.filter(election__office__office='COUNCIL AT LARGE', candidate__party="Democrat").values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes')

        # Retrive At Large Republican candidates and votes
        sum_votes_by_candidate_atlarge_reps = current_election.filter(election__office__office='COUNCIL AT LARGE', candidate__party="Republican").values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes')

        # Retrieve At Large Other Party candidates and votes
        sum_votes_by_candidate_atlarge_other = current_election.filter(election__office__office='COUNCIL AT LARGE').values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes').exclude(candidate__party__in=["Democrat", "Republican"])
     
        # Retrieve district candidates and votes
        sum_votes_by_candidate_district = current_election.filter(election__office__office__startswith='DIST').values('election__office__office',  'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_votes = Sum('vote_count')).order_by('-total_votes')



        sum_votes_by_office = current_election.all().values('election__office__office').annotate(Sum('vote_count'))

        sum_votes_by_office_district = current_election.filter(election__office__office__startswith='DIST').values('election__office__office').annotate(Sum('vote_count'))

    except KeyError:
        print("ELECTION YEAR: ", election_year)
        print("TYPE: ", type(election_year))
        # print("FROM DICT: ", elections[election_year])
        return HttpResponse("That is not a valid year")
    except TypeError:
        return HttpResponse("Select a year")



    context = {
        # "sum_votes_by_candidate":sum_votes_by_candidate,
        "sum_votes_by_candidate_atlarge_dems":sum_votes_by_candidate_atlarge_dems,
        "sum_votes_by_candidate_atlarge_reps":sum_votes_by_candidate_atlarge_reps,
        "sum_votes_by_candidate_atlarge_other":sum_votes_by_candidate_atlarge_other,
        "sum_votes_by_candidate_district":sum_votes_by_candidate_district,
        "sum_votes_by_office_district":sum_votes_by_office_district,
        "sum_votes_by_candidate_atlarge_other": sum_votes_by_candidate_atlarge_other,
        "election_year": election_year,


    }

    return render(request, 'phlcitycouncil/vote_count.html', context)


def candidate_bios(request, user_id):
    user = Person.objects.get(id=user_id)
    user_gender = user.gender

    if user.race:
        user_race = user.race
    else:
        user_race = "unknown"


    if user.birthdate:
        user_birthdate = user.birthdate
    else:
        user_birthdate = "unknown"




    context = {
    "user":user,
    "user_id":user_id,
    "user_gender":user_gender,
    "user_race":user_race,
    "user_birthdate":user_birthdate,
    }

    return render(request, 'phlcitycouncil/candidate_bios.html', context)
    
    # HARD CODED HTML to be returned
    # return HttpResponse("Vistiing phlcitycouncil. <br>" + str(user_id) + " is the id for  " + str(user))


def candidate_list(request):
    candidates = Candidate.objects.all()
    print("$" * 100)
    print(candidates)

    context = {"candidates":candidates}

    return render(request, 'phlcitycouncil/candidate_list.html', context)

def about(request):
    return HttpResponse('the about page')