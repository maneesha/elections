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


    def overlapping_terms(self):
        # # Raise error if: 
        # # This candidate's start date for this office < this candidate's end date for another term/office  
        # # This candidate's end date for this office > this candidate's start date for another term/office
        # # This candidate's start date for this office < another candidate's end date for this office
        # # This candidate's end date for this office > another candidate's start date for this office 
        # # negate does it not overlap - may be easier than checking they do
        # print("THE CREATED START DATE IS: ", self.start_date)
        # print("THE CREATED END DATE IS: ", self.end_date)
        # print("THE CREATED CANDIDATE IS: ", self.candidate_id, self.candidate)
        # print("THE CREATED OFFICE IS: ", self.office_id, self.office)
        # # print("OBJECTS WHERE START DATE IS GREATER THAN SELF START DATE")
        # #  print(Term.objects.filter(start_date__lte = self.start_date))
        # print("##########")


        # # Check to see if that candidate has any overlapping dates
        # if Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)).exists():

        #     print("THERE IS AN ERROR WITH OVERLAPPING DATES FOR THIS CANDIDATE")
        #     print(Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)))

        #     xx = Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)).exists()
        #     print(xx)


        #     print("END OVERLAPPING CANDIDATE ERROR")
        #     # print("### FILTERED Q: ", Term.objects.filter(Q(candidate_id = self.candidate_id)), "#### END")

        # # Check to see if that office has any overlapping dates
        # if Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)).exists():

        #     print("THERE IS AN ERROR WITH OVERLAPPING DATES FOR THIS OFFICE")
        #     print(Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)))
        #     print("END OVERLAPPING OFFICE ERROR")



        if Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)).exists():

            print("this is where validation error should go")
            raise ValidationError("Overlapping dates for Candidate")

        if Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)).exists():
            
            print("this is where validation error should go")
            raise ValidationError("Overlapping dates for Office")


        return self.candidate, self.office, self.start_date, self.end_date



    def clean(self):

        try:
            self.overlapping_terms()
        except ValidationError:
            print("### THIS IS A VALIDATION ERROR ###")

        # if Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)).exists():

        #     print("this is where validation error should go")
        #     raise ValidationError("Overlapping dates for Candidate")

        # if Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__gt=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lt=self.end_date)).exists():
            
        #     print("this is where validation error should go")
        #     raise ValidationError("Overlapping dates for Office")

        # if Term.objects.filter(Q(start_date__gte=self.start_date, start_date__lt=self.end_date) | Q(end_date__gt=self.start_date, end_date__lte=self.end_date)).exists():
        #     raise ValidationError("Overlapping dates")

        # pass
        

    

    def test_method(self):
        # Get all of this candidate's records
        q = Term.objects.all().filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__lt = self.start_date))

        print("This is the test method")        
        print(self.candidate)

        print("another line")
        print("query: ", q)
        print("last line")


        # pass


    # def clean():
    #     pass

    def __str__(self):
        return '%s, %s, start: %s, end: %s, %s' % (self.candidate, self.office, self.start_date, self.end_date, self.departed)




