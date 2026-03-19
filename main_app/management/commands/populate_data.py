from django.core.management.base import BaseCommand
from main_app.models import Customer, Policy, Claim, Payment, User
from random import randint
from faker import Faker
from datetime import timedelta
import random
import string

fake = Faker()

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create dummy users
        for _ in range(10):  # Create 10 users
            user = User.objects.create_user(  # Assuming a custom User model
                username=fake.user_name(),
                password='password123',  # You can set a default password
                email=fake.email(),
            )
            
            # Create dummy customers
            customer = Customer.objects.create(
                name=fake.name(),
                email=fake.email(),
                phone_number=fake.phone_number()[:15],
                address=fake.address(),
                date_of_birth=fake.date_of_birth(),
                gender=fake.random_element(['Male', 'Female']),
            )

            # Create dummy policies
            start_date = fake.date_this_decade()  # Random start date
            end_date = start_date + timedelta(days=randint(365, 3650))  # End date between 1 and 10 years after start date
            
            # Generate a unique policy number with a length of 15 characters
            while True:
                policy_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))  # Random 15-character string
                if not Policy.objects.filter(policy_number=policy_number).exists():
                    break  # Exit the loop once a unique policy_number is found

            # Create the policy object
            policy = Policy.objects.create(
                policy_number=policy_number,  # Set the unique 15-character policy number
                customer=customer,
                policy_type=fake.random_element(['Health', 'Auto', 'Life', 'Property']),
                status=fake.random_element(['Active', 'Expired', 'Cancelled']),
                coverage_amount=randint(5000, 50000),
                premium=randint(100, 1000),
                start_date=start_date,
                end_date=end_date,  # Set the end date
                user=user,  # Set the user here (this was missing)
            )

            # Create dummy claims
            claim_number = f"CLAIM-{fake.unique.random_number(digits=5)}"  # Generate unique claim number
            status = random.choice(['Pending', 'Approved', 'Rejected', 'Paid'])  # Choose status randomly
            claim = Claim.objects.create(
                policy=policy,  # Link claim to the created policy
                claim_number=claim_number,  # Unique claim number
                amount=randint(1000, 50000),  # Random claim amount
                reason=fake.text(),  # Random reason for the claim
                status=status,  # Random status
            )

            # Create dummy payments
            Payment.objects.create(
                customer=customer,  # Link to the created customer
                policy=policy,  # Link to the created policy
                amount=randint(100, 1000),  # Random payment amount
                payment_date=fake.date_this_decade(),  # Random payment date within the last decade
                transaction_type=fake.random_element(['Credit', 'Debit']),  # Random transaction type ('Credit' or 'Debit')
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data!'))
