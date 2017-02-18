from django.db import models

from django.db.models import Q

from django.core.exceptions import ValidationError

from django.db.models import Count, Sum, Max

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

    class Meta:
        ordering =('last_name', 'first_name')

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
        ordering = ('person',)


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

    OFFICE_TYPE_CHOICES = (
        ('District', 'District'),
        ('At-Large', 'At-Large')
        )


    office_type = models.CharField(max_length = 10, choices = OFFICE_TYPE_CHOICES)

    def __str__(self):
        return self.office

    class Meta:
        ordering = ('office',)

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


    def show_winner(dist):
        return Vote.objects.filter(election__office__office=dist).values('election__office__office', 'candidate__person__last_name', 'candidate__person__first_name', 'candidate__party').annotate(total_vote=Sum('vote_count')).order_by('-total_vote').first()





class Term(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    

    SEAT_CHOICES = (

          ("DISTRICT COUNCIL - 1ST DISTRICT", "DISTRICT COUNCIL - 1ST DISTRICT"),
          ("DISTRICT COUNCIL - 2ND DISTRICT", "DISTRICT COUNCIL - 2ND DISTRICT"),
          ("DISTRICT COUNCIL - 3RD DISTRICT", "DISTRICT COUNCIL - 3RD DISTRICT"),
          ("DISTRICT COUNCIL - 4TH DISTRICT", "DISTRICT COUNCIL - 4TH DISTRICT"),
          ("DISTRICT COUNCIL - 5TH DISTRICT", "DISTRICT COUNCIL - 5TH DISTRICT"),
          ("DISTRICT COUNCIL - 6TH DISTRICT", "DISTRICT COUNCIL - 6TH DISTRICT"),
          ("DISTRICT COUNCIL - 7TH DISTRICT", "DISTRICT COUNCIL - 7TH DISTRICT"),
          ("DISTRICT COUNCIL - 8TH DISTRICT", "DISTRICT COUNCIL - 8TH DISTRICT"),
          ("DISTRICT COUNCIL - 9TH DISTRICT", "DISTRICT COUNCIL - 9TH DISTRICT"),
          ("DISTRICT COUNCIL - 10TH DISTRICT", "DISTRICT COUNCIL - 10TH DISTRICT"),    
          ("COUNCIL AT LARGE SEAT 1", "COUNCIL AT LARGE SEAT 1" ),
          ("COUNCIL AT LARGE SEAT 2", "COUNCIL AT LARGE SEAT 2" ),
          ("COUNCIL AT LARGE SEAT 3", "COUNCIL AT LARGE SEAT 3"),
          ("COUNCIL AT LARGE SEAT 4", "COUNCIL AT LARGE SEAT 4"),
          ("COUNCIL AT LARGE SEAT 5", "COUNCIL AT LARGE SEAT 5"),
          ("COUNCIL AT LARGE SEAT 6", "COUNCIL AT LARGE SEAT 6"),
          ("COUNCIL AT LARGE SEAT 7", "COUNCIL AT LARGE SEAT 7"),

          )



    seat = models.CharField(max_length = 50, null=True, blank=True, choices = SEAT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    DEPARTED_CHOICES = (
        ('Incumbent', 'Incumbent'),     # Currently in office
        ('Re-elected', 'Re-elected'),   # Ran for reelection and won
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



        # Ensure term is not 4 years + 1 week long (for changes in inauguration day)

        term_length = self.end_date - self.start_date
        if term_length.days < 1469:
            print("###############DATE DIFF < 4 YRS: ##############", term_length)
            type(term_length)
        else:
            raise ValidationError("Term must be shorter than 1469 days (4 years + 1 week cushion)")



        # Ensure incumbents don't have an end date < today

        if self.departed == "Incumbent" and self.end_date < datetime.date.today():
            raise ValidationError("An incumbent must have an end date in the future.")


        # CHECKING FOR CANDIDATE AND OFFICE OVERLAPPING DATES

        matching_candidate_records = Term.objects.filter(Q(candidate_id = self.candidate_id))
        matching_seat_records = Term.objects.filter(Q(seat = self.seat))


        # No candidate or office overlaps - GOOD! If these conditions are met, pass.
        candidate_no_overlaps_before = matching_candidate_records.filter(Q(start_date__gt = self.start_date), Q(start_date__gte = self.end_date))
        candidate_no_overlaps_after = matching_candidate_records.filter(Q(end_date__lte = self.start_date))
        seat_no_overlaps_before = matching_seat_records.filter(Q(start_date__gt = self.start_date), Q(start_date__gte = self.end_date))
        seat_no_overlaps_after = matching_seat_records.filter(Q(end_date__lte = self.start_date))

        # Overlap(s) exist(s) - BAD!  Check to see where it overlaps.

        # Candidate or Office New term starts on same day as existing term
        candidate_same_start_date = matching_candidate_records.filter(Q(start_date = self.start_date))
        seat_same_start_date = matching_seat_records.filter(Q(start_date = self.start_date))

        # Candidate New term starts before but ends during or after existing term
        candidate_ends_during_or_after = matching_candidate_records.filter(Q(start_date__gt = self.start_date), Q(start_date__lt = self.end_date))
        seat_ends_during_or_after = matching_seat_records.filter(Q(start_date__gt = self.start_date), Q(start_date__lt = self.end_date))

        # Candidate New term starts during an existing term
        candidate_starts_during_existing = matching_candidate_records.filter(Q(start_date__lt = self.start_date), Q(end_date__gt = self.start_date))
        seat_starts_during_existing = matching_seat_records.filter(Q(start_date__lt = self.start_date), Q(end_date__gt = self.start_date))



        # This is the first record being entered for this candidate
        if len(matching_candidate_records) == 0:
            print("No existing records for this candidate")
            # pass

        # Candidate dates don't overlap; pass
        elif candidate_no_overlaps_before.exists() or candidate_no_overlaps_after.exists():
            print("NO OVERLAPS BEFORE: ", candidate_no_overlaps_before)
            print("NO OVERLAPS AFTER: ", candidate_no_overlaps_after)
            # pass

        # Raise validataion error for different kinds of candidate overlaps
        elif candidate_same_start_date.exists():
            print("There is another record for this candidate with the same start date")
            raise ValidationError(("There is another record for this candidate with the same start date", candidate_same_start_date))

        elif candidate_ends_during_or_after.exists():
            print("The new record's end date is during or after an existing record")
            raise ValidationError(("The new record's end date is during or after an existing candidate record", candidate_ends_during_or_after))

        elif candidate_starts_during_existing.exists():
            print("A new record can not start during an existing record")
            raise ValidationError(("A new candidate record can not start during an existing candidate record", candidate_starts_during_existing))

        else:
            print("MATCHING CANDIDATE RECORDS: ", matching_candidate_records, "LENGTH: ", len(matching_candidate_records))
            raise ValidationError("Something unknown went wrong.")    



        # This is the first record being entered for this seat
        if len(matching_seat_records) == 0:
            print("No existing records for this seat")
            # pass



        # Seat dates don't overlap; pass
        elif seat_no_overlaps_before.exists() or seat_no_overlaps_after.exists():
            print("NO OVERLAPS BEFORE: ", seat_no_overlaps_before)
            print("NO OVERLAPS AFTER: ", seat_no_overlaps_after)
            # pass

        # Raise validataion error for different kinds of seat overlaps
        elif seat_same_start_date.exists():
            print("There is another record for this seat with the same start date")
            raise ValidationError(("There is another record for this seat with the same start date", seat_same_start_date))

        elif seat_ends_during_or_after.exists():
            print("The new record's end date is during or after an existing seat record")
            raise ValidationError(("The new record's end date is during or after an existing seat record", seat_ends_during_or_after))

        elif seat_starts_during_existing.exists():
            print("A new seat record can not start during an existing seat record")
            raise ValidationError(("A new seat record can not start during an existing seat record", seat_starts_during_existing))

        else:
            print("MATCHING SEAT RECORDS: ", matching_seat_records, "LENGTH: ", len(matching_seat_records))
            raise ValidationError("Something unknown went wrong.")    




        # Place candidates in seat based on office
        # if office_type == district: 
        #     seat must = office
        # if office_type == at_large:
        #     seat is manually assigned



        if self.office.office_type == "District":
            if str(self.office) != self.seat:
                print("SEAT must match OFFICE for district records")
                raise ValidationError("SEAT must match OFFICE for district records")
        if self.office.office_type == "At-Large":
            # Office will be just "At Large" while seat will be "At Large 1", "At Large 2", etc.
            if self.seat not in ["COUNCIL AT LARGE SEAT 1", "COUNCIL AT LARGE SEAT 2", "COUNCIL AT LARGE SEAT 3", "COUNCIL AT LARGE SEAT 4", "COUNCIL AT LARGE SEAT 5", "COUNCIL AT LARGE SEAT 6", "COUNCIL AT LARGE SEAT 7"]:
                print("SEAT must be one of the at large seats.")
                raise ValidationError("SEAT must be one of the at large seats.")

        print("#"*20)
        print("YOU HAVE CREATED A NEW RECORD WITH: ")
        print("OFFICE: ", self.office)
        print("SEAT: ", self.seat)
        print("OFFICE TYPE: ", self.office.office_type)
        print("#"*20)



# ["COUNCIL AT LARGE SEAT 1", "COUNCIL AT LARGE SEAT 2", "COUNCIL AT LARGE SEAT 3", "COUNCIL AT LARGE SEAT 4", "COUNCIL AT LARGE SEAT 5", "COUNCIL AT LARGE SEAT 6", "COUNCIL AT LARGE SEAT 7"]










        ######################    
        # How'd they leave? Conditions to check for:
        # If Died, can't have a future term
        # If Incumbent, can't have a future term
        # If Defeated, can't have an immediately future term
        # If Re-elected, must have an immediately future term (but how to do this if you enter the next term afterwards?)    

        print("*" * 50)
        print("HOW'D THEY LEAVE?")
        print(matching_candidate_records.filter(departed = 'Died'))
        print("*" * 50)
        #####################








    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)