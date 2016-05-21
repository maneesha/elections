from django.db import models

# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length = 50)
    middle_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50)
    suffix = models.CharField(max_length=10, null = True, blank = True)
    birthdate = models.DateField(null = True, blank = True)
    
    RACE_CHOICES = (
        ('Asian', 'Asian'), 
        ('Black', 'Black'),
        ('Hispanic', 'Hispanic'),
        ('White', 'White')
    )

    race = models.CharField(max_length = 20, choices = RACE_CHOICES, null = True, blank = True)


    GENDER_CHOICES = (
        ('Female', 'Female'),
        ('Male', 'Male')
        )

    gender = models.CharField(max_length = 6, choices = GENDER_CHOICES, null = True, blank = True)
    notes = models.TextField(null = True, blank = True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def is_not_white(self):
        return self.race != 'White'

class Candidate(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    PARTY_CHOICES = (
        ('Democrat', 'Democrat'),
        ('Republican', 'Republican')
        )

    party = models.CharField(max_length = 12, choices = PARTY_CHOICES)

    class Meta:
        unique_together = ('person', 'party',)


    def __str__(self):
        return '%s, %s' % (self.person, self.party)

class District(models.Model):
    ward = models.CharField(max_length = 2)
    division = models.CharField(max_length = 2)

    class Meta:
        unique_together = ('ward', 'division')



    def __str__(self):
        return '%s%s' % (self.ward, self.division)

class Office(models.Model):
    office = models.CharField(max_length = 50)

    def __str__(self):
        return self.office

class Election(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    election_date = models.DateField()
    office = models.ForeignKey(Office, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s, %s' % (self.district, self.election_date, self.office)

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    vote_count = models.IntegerField(null = True, blank = True)

    class Meta:
        unique_together = ('candidate', 'election',)

    def __str__(self):
        return '%s %s %s' % (self.candidate, self.election, self.vote_count)

class Term(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    effective_start_year = models.IntegerField()
    effecive_end_year = models.IntegerField()
    departed = models.CharField(max_length = 25)
    notes = models.TextField(null = True, blank = True)

    def eff_start_year(self):
        if self.start_date.month <= 10:
            return self.start_date.year 
        elif self.start_date.month >= 11:
            return self.start_date.year + 1
        
    def eff_end_year(self):
        if self.end_date.month <= 2:
            return self.end_date.year - 1
        elif self.end_date.month >= 3:
            return self.end_date.year

    def __str__(self):
        return '%s %s %s %s %s' % (self.candidate, self.office, self.effective_start_year, self.effecive_end_year, self.departed)



