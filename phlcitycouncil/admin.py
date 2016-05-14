from django.contrib import admin

# Register your models here.

from .models import Person, Candidate, District, Election, Vote, Term, Office

admin.site.register([Person, Candidate, District, Election, Vote, Term, Office])


