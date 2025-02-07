from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Custom User Model
class User(AbstractUser):  # Extends Django's built-in User model
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_agent = models.BooleanField(default=False)  # To differentiate between customers and agents
    
    def __str__(self):
        return self.username

# Policy Model
class Policy(models.Model):
    POLICY_TYPES = [
        ('Health', 'Health Insurance'),
        ('Auto', 'Auto Insurance'),
        ('Home', 'Home Insurance'),
        ('Life', 'Life Insurance'),
    ]
    
    name = models.CharField(max_length=255, default='Default Name')
    policy_number = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='policies')
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
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.payment_date} - {self.amount}"

# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

# Agent Model
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
