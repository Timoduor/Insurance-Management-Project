from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date


# Custom User Model
class User(AbstractUser):
    # Add custom fields to the User model

    date_of_birth = models.DateField(default=date.today, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[('Customer', 'Customer'), ('Agent', 'Agent'), ('Admin', 'Admin')],
        default='Customer'
    )
    
    def __str__(self):
        return self.username  # You can return a custom string representation here


# Policy Model
class Policy(models.Model):
    POLICY_TYPES = [
        ('Health', 'Health Insurance'),
        ('Auto', 'Auto Insurance'),
        ('Home', 'Home Insurance'),
        ('Life', 'Life Insurance'),
    ]
    
    name = models.CharField(max_length=255, default='Default Name')
    
    # Use the ForeignKey relationship with Customer here
    customer = models.ForeignKey('main_app.Customer', on_delete=models.CASCADE, null=True)  # Use a string reference
    policy_number = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey('main_app.User', on_delete=models.CASCADE, related_name='policies')
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=[('Active', 'Active'), ('Expired', 'Expired'), ('Cancelled', 'Cancelled')], default='Active'
    )
    
    def __str__(self):
        return f"{self.policy_number} - {self.policy_type}"

# Claim Model
class Claim(models.Model):
    CLAIM_STATUSES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Paid', 'Paid'),
    ]

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)  # Allow null if no policy is set yet
    claim_number = models.CharField(max_length=50, unique=True)
    claim_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reason = models.CharField(max_length=255, default='DEFAULT_REASON')
    status = models.CharField(max_length=20, choices=CLAIM_STATUSES, default='Pending')
    
    def __str__(self):
        return f"{self.claim_number} - {self.status}"

# Insurance Plan Model
class InsurancePlan(models.Model):
    plan_name = models.CharField(max_length=100)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_premium = models.DecimalField(max_digits=10, decimal_places=2)

# Payment Model
class Payment(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)  # Link to Customer model
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)  # Link to Policy model
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount (up to 10 digits)
    payment_date = models.DateField()  # Date of payment
    transaction_type = models.CharField(
        max_length=10, 
        choices=[('Credit', 'Credit'), ('Debit', 'Debit')],
        default='Credit'  # Move default inside the field definition
    )  # Transaction type (either 'Credit' or 'Debit')

    def __str__(self):
        return f"Payment for {self.customer} on {self.payment_date}"



# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)  # Add this field
    address = models.TextField()
    date_of_birth = models.DateField(default=date.today)
    gender =  models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')  # Default added here

    def __str__(self):
        return self.name

# Agent Model
class Agent(models.Model):
    user = models.OneToOneField('main_app.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    agency = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Transaction Model
class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.policy.policy_number} - {self.amount}"
