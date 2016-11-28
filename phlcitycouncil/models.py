from django.db import models

from django.db.models import Q

from django.core.exceptions import ValidationError

import datetime


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

    BALLOT_TYPE_CHOICES = (
        ('A', 'Absentee'),
        ('P', 'Provisional'),
        ('M', 'Machine'),
        )

    ballot_type = models.CharField(max_length = 50, null=True, blank=True, choices = BALLOT_TYPE_CHOICES)


    class Meta:
        unique_together = ('candidate', 'election', 'ballot_type')

    def __str__(self):
        return '%s %s %s' % (self.candidate, self.election, self.vote_count)

    def clean(self):

        if self.vote_count < 0:
            raise ValidationError("Vote count must be an integer 0 or greater.")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


    

class Term(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    DEPARTED_CHOICES = (
        ('Incumbent', 'Incumbent'),     # Currently in office
        ('Defeated', 'Defeated'),       # Ran for reelection and was defeated
        ('Retired', 'Retired'),         # Decided not to run for reelction; served through current term
        ('Resigned', 'Resigned'),       # Resigned to take another position during current term
        ('Scandal', 'Scandal'),         # Resigned amidst a scandal
        ('Died', 'Died'),               # Died in office
        )


    departed = models.CharField(max_length = 25, choices = DEPARTED_CHOICES)
    notes = models.TextField(null = True, blank = True)

    class Meta:
        unique_together = ('candidate', 'office', 'start_date', 'end_date', 'departed')


    def __str__(self):
        return '%s, %s, start: %s, end: %s, %s' % (self.candidate, self.office, self.start_date, self.end_date, self.departed)

    def clean(self):

        # Ensure start date is earlier than end date

        if self.start_date > self.end_date:
            raise ValidationError("Start date must be equal to or earlier than end date")


        # Ensure incumbents don't have an end date < today

        if self.departed == "Incumbent" and self.end_date < datetime.date.today():
            raise ValidationError("An incumbent must have an end date in the future.")





        # No overlaps - GOOD! If these conditions are met, pass.
        no_overlaps_before = Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__lt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__lt = self.start_date), Q(end_date__lt = self.end_date))

        no_overlaps_after = Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt = self.start_date), Q(start_date__gt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__gt = self.end_date))


        # Overlap(s) exist(s) - BAD!  Check to see where it overlaps.

        # New candidate record is entirely inside an existing candidate record
        overlapping_candidate_inner = Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__lt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__gt = self.end_date))

        # New candidate record is outside an entire exisiting candidate record
        overlapping_candidate_outer = Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__lt = self.end_date))

        # New candidate record ends during existing candidate record
        overlapping_candidate_left = Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__gt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__gt = self.end_date))

        # New candidate record starts during existing candidate record
        overlapping_candidate_right = Term.objects.filter(Q(candidate_id = self.candidate_id)).filter(Q(start_date__lt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__gt = self.end_date))

        # New office record is entirely inside an existing office record 
        overlapping_office_inner = Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__lt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__gt = self.end_date))

        # New office record is outside an entire existing office record
        overlapping_office_outer = Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__gt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__lt = self.end_date))

        # New office record ends during an existing office record
        overlapping_office_left = Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__gt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__gt = self.end_date))

        # New office record starts during an existing office record
        overlapping_office_right = Term.objects.filter(Q(office_id = self.office_id)).filter(Q(start_date__lt = self.start_date), Q(start_date__lt = self.end_date), Q(end_date__gt = self.start_date), Q(end_date__gt = self.end_date))



        if no_overlaps_before.exists() or no_overlaps_after.exists():
            pass


        elif overlapping_candidate_inner.exists():
            print("This term overlaps another term for this candidate")
            raise ValidationError(("A new term can not be entirely inside an existing term", overlapping_candidate_inner))

        elif overlapping_candidate_outer.exists():
            print("This term overlaps another term for this candidate")
            raise ValidationError(("A new term can not entirely include another term", overlapping_candidate_outer))

        elif overlapping_candidate_left.exists():
            print("This term overlaps another term for this candidate")
            raise ValidationError(("A new term can not end during another term", overlapping_candidate_left))

        elif overlapping_candidate_right.exists():
            print("This term overlaps another term for this candidate")
            raise ValidationError(("A new term can not begin during another term", overlapping_candidate_right))



        elif overlapping_office_inner.exists():
            print("This term overlaps another term for this candidate")
            raise ValidationError(("A new term can not be entirely inside an existing term", overlapping_office_inner))
        
        elif overlapping_office_outer.exists():
            print("This term overlaps another term for this candidate")
            raise ValidationError(("A new term can not entirely include another term", overlapping_office_outer))


        elif overlapping_office_left.exists():
            print("This term overlaps another term for this office")
            raise ValidationError(("A new term can not end during another term", overlapping_office_left))


        elif overlapping_office_right.exists():
            print("This term overlaps another term for this office")
            raise ValidationError(("A new term can not begin during another term", overlapping_office_left))


    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)