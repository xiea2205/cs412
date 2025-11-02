"""
Name: Anthony Xie
Email: anthoxie@bu.edu
Description: Models for the voter_analytics application. Contains the Voter model
representing voter registration data from Newton, MA, and a load_data function
to import voter data from CSV.
"""

from django.db import models
import csv
from datetime import datetime


class Voter(models.Model):
    """
    Model representing a registered voter in Newton, MA.
    Contains demographic information, party affiliation, and voting history.
    """
    # Personal Information
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)

    # Residential Address
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=10)

    # Registration Information
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)

    # Voting History (past 5 elections)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # Voter Score (count of elections attended)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """String representation of the Voter."""
        return f"{self.first_name} {self.last_name} - {self.street_number} {self.street_name}"


def load_data():
    """
    Load voter data from the CSV file into the database.
    Clears existing voter records and imports fresh data from newton_voters.csv.
    """
    # Delete all existing records
    Voter.objects.all().delete()

    # Path to the CSV file
    csv_file_path = 'newton_voters.csv'

    print(f"Loading data from {csv_file_path}...")

    # Open and read the CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        count = 0
        for row in reader:
            try:
                # Parse dates
                dob = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date()
                dor = datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date()

                # Create Voter object
                voter = Voter(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row['Residential Address - Apartment Number'] if row['Residential Address - Apartment Number'] else None,
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=dob,
                    date_of_registration=dor,
                    party_affiliation=row['Party Affiliation'],
                    precinct_number=row['Precinct Number'],
                    v20state=row['v20state'] == 'TRUE',
                    v21town=row['v21town'] == 'TRUE',
                    v21primary=row['v21primary'] == 'TRUE',
                    v22general=row['v22general'] == 'TRUE',
                    v23town=row['v23town'] == 'TRUE',
                    voter_score=int(row['voter_score'])
                )
                voter.save()

                count += 1
                if count % 1000 == 0:
                    print(f"Loaded {count} voters...")

            except Exception as e:
                print(f"Error loading row: {e}")
                print(f"Row data: {row}")
                continue

    print(f"Done! Loaded {count} voters.")
