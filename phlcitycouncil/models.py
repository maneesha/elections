from django.db import models

from django.db.models import Q

from django.core.exceptions import ValidationError


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
        ('Green', 'Green'),
        ('Free Dominion Party', 'Free Dominion Party'),
        ('Independent', 'Independent'),
        ('Philadelphia Party',  'Philadelphia Party'),
        ('Republican', 'Republican'),
        ('Socialist Workers Party', 'Socialist Workers Party'),
        )

    party = models.CharField(max_length = 35, choices = PARTY_CHOICES)

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
        return 'Ward: %s, Division: %s' % (self.ward, self.division)

class Office(models.Model):
    office = models.CharField(max_length = 50)

    def __str__(self):
        return self.office

class Election(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    election_date = models.DateField()
    office = models.ForeignKey(Office, on_delete=models.CASCADE)

    ELECTION_TYPE_CHOICES = (
        ('General', 'General'),
        ('Primary', 'Primary'),
        ('Special', 'Special')
        )

    election_type = models.CharField(max_length = 50, null=True, blank=True, choices = ELECTION_TYPE_CHOICES)

    def __str__(self):
        return '%s %s, %s %s' % (self.district, self.election_date, self.office, self.election_type)

class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    vote_count = models.IntegerField(null = True, blank = True)

    # to be absentee, provisional, machine
    ballot_type = models.CharField(max_length = 50, null=True, blank=True)

    class Meta:
        unique_together = ('candidate', 'election', 'ballot_type')

    def __str__(self):
        return '%s %s %s' % (self.candidate, self.election, self.vote_count)

class Term(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    departed = models.CharField(max_length = 25)
    notes = models.TextField(null = True, blank = True)

    class Meta:
        unique_together = ('candidate', 'office', 'start_date', 'end_date', 'departed')

    ## ADD CHOICES FOR departed 


    def clean(self):

        #This logic needs work.
        #Does not work when overlaps are within another range -- only when the overlap extends out of the range
        #Example:  
        #Range 1 = 1 to 10
        #Range 2 = 8 to 12
        #Range 3 = 4 to 10
        #Range 2 will return error; Range 3 will not


        overlapping_candidate_check = Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date))

 

        if overlapping_candidate_check.exists():

            print("####    LOG ####")
            print(overlapping_candidate_check)
            print("### END LOG ###")

            print("This term overlaps another term for this candidate")
            raise ValidationError("Overlapping dates for Candidate", overlapping_candidate_check)


        overlapping_office_check = Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date))

        if overlapping_office_check.exists():

            print("####    LOG ####")
            print(overlapping_office_check)
            print("### END LOG ###")            
            
            print("This term overlaps another term for this office")
            raise ValidationError("Overlapping dates for Office", overlapping_office_check)


    def test_method(self):
        # Get all of this candidate's records
        q = Term.objects.all().filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__lt = self.start_date))

        print("This is the test method")        
        print(self.candidate)

        print("another line")
        print("query: ", q)
        print("last line")


    def __str__(self):
        return '%s, %s, start: %s, end: %s, %s' % (self.candidate, self.office, self.start_date, self.end_date, self.departed)




    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)