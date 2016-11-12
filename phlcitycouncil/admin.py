from django.contrib import admin
from django.db import models


# Register your models here.

from .models import Person, Candidate, District, Election, Vote, Term, Office

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthdate', 'gender')

class TermAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'start_date', 'end_date',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('ward', 'division')

class ElectionAdmin(admin.ModelAdmin):
    list_display = ('district', 'election_date', 'office', 'election_type')

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('person', 'party')

admin.site.register(Person, PersonAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Vote)
admin.site.register(Term, TermAdmin)
admin.site.register(Office)

