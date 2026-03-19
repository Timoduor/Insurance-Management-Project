from django.db.models import Count, Sum
from .models import Policy, Claim, Payment, Customer

def get_policy_statistics():
    """
    Get statistics for all policies.
    """
    total_policies = Policy.objects.count()
    active_policies = Policy.objects.filter(status='Active').count()
    expired_policies = Policy.objects.filter(status='Expired').count()
    cancelled_policies = Policy.objects.filter(status='Cancelled').count()
    
    return {
        'total_policies': total_policies,
        'active_policies': active_policies,
        'expired_policies': expired_policies,
        'cancelled_policies': cancelled_policies,
    }

def get_claim_statistics():
    """
    Get statistics for all claims.
    """
    total_claims = Claim.objects.count()
    approved_claims = Claim.objects.filter(status='Approved').count()
    pending_claims = Claim.objects.filter(status='Pending').count()
    rejected_claims = Claim.objects.filter(status='Rejected').count()
    paid_claims = Claim.objects.filter(status='Paid').count()

    return {
        'total_claims': total_claims,
        'approved_claims': approved_claims,
        'pending_claims': pending_claims,
        'rejected_claims': rejected_claims,
        'paid_claims': paid_claims,
    }

def get_payment_statistics():
    """
    Get statistics for all payments.
    """
    total_payments = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_transactions = Payment.objects.count()

    return {
        'total_payments': total_payments,
        'total_transactions': total_transactions,
    }

def get_customer_claim_statistics():
    """
    Get number of claims per customer.
    """
    customer_claims = Customer.objects.annotate(num_claims=Count('claim')).values('id', 'name', 'num_claims')
    
    return customer_claims

def get_claims_by_policy_type():
    """
    Get number of claims per policy type.
    """
    claims_by_policy_type = Claim.objects.values('policy__policy_type').annotate(total_claims=Count('id'))
    
    return claims_by_policy_type

def get_analytics_summary():
    """
    Get an overall summary of analytics.
    """
    policy_stats = get_policy_statistics()
    claim_stats = get_claim_statistics()
    payment_stats = get_payment_statistics()
    
    return {
        'policy_stats': policy_stats,
        'claim_stats': claim_stats,
        'payment_stats': payment_stats
    }
