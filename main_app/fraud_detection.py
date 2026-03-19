from datetime import timedelta
from django.utils import timezone
from .models import Claim, Payment

def detect_fraud(customer):
    # Check for multiple claims in the last 30 days
    recent_claims = Claim.objects.filter(
        customer=customer,
        claim_date__gte=timezone.now() - timedelta(days=30)
    )

    # Rule: More than 3 claims in the last 30 days
    if recent_claims.count() > 3:
        return True  # Fraud detected: Too many claims in a short period
    
    # Check for unusually high payments (e.g., more than $5000 in total payments)
    total_payments = Payment.objects.filter(customer=customer).aggregate(Sum('amount'))['amount__sum']
    
    if total_payments and total_payments > 5000:  # Example threshold for fraud detection
        return True  # Fraud detected: Unusually high total payments
    
    return False  # No fraud detected
