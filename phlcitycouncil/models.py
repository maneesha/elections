from django.db import models

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length = 50)
    middle_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50)
    birthdate = models.DateTimeField(null = True, blank = True)
    race = models.CharField(max_length = 20, null = True, blank = True)
    gender = models.CharField(max_length = 6, null = True, blank = True)
    notes = models.TextField(null = True, blank = True)

    def __str__(self):
        return '%s, %s' % (self.first_name, self.last_name)

    def is_not_white(self):
        return self.race != 'White'

class Candidate(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    party = models.CharField(max_length = 12)

    def __str__(self):
        return '%s, %s' % (self.person, self.party)

class District(models.Model):
    district_number = models.CharField(max_length = 10)
    state = models.CharField(max_length = 2)

    def __str__(self):
        return '%s %s' % (self.district_number, self.state)

class Office(models.Model):
    office = models.CharField(max_length = 50)

    def __str__(self):
        return self.office

class Election(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    election_date = models.DateTimeField()
    office = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.district, self.election_date, self.office)

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    vote_count = models.IntegerField(null = True, blank = True)

    def __str__(self):
        return '%s %s %s' % (self.candidate, self.election, self.vote_count)

class Term(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    effective_start_year = models.IntegerField()
    effecive_end_year = models.IntegerField()
    departed = models.CharField(max_length = 25)
    notes = models.TextField(null = True, blank = True)

    def __str__(self):
        return '%s %s %s %s %s' % (self.candidate, self.office, self.effective_start_year, self.effecive_end_year, self.departed)



