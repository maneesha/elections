from django.db import models

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length = 50)
    middle_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50, null = True, blank = True)
    birthdate = models.DateTimeField()
    race = models.CharField()
    gender = models.CharField()
    notes = models.TextField()

class Candidate(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    party = models.CharField(max_length = 12)

class District(models.Model):
    district_number = models.CharField(max_length = 10)
    state = models.CharField(max_length = 2)

class Election(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    election_date = models.DateTimeField()
    office = models.CharField(max_length = 50)

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    