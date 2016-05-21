from django.contrib import admin
from django.db import models


# Register your models here.

from .models import Person, Candidate, District, Election, Vote, Term, Office

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthdate', 'gender')

class TermAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'start_date', 'end_date', 'eff_start_year', 'eff_end_year')

admin.site.register(Person, PersonAdmin)
admin.site.register(Candidate)
admin.site.register(District)
admin.site.register(Election)
admin.site.register(Vote)
admin.site.register(Term, TermAdmin)
admin.site.register(Office)
