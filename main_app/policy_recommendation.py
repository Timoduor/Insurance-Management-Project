from .models import Policy, Customer

def recommend_policy_for_customer(customer):
    """
    Generate policy recommendations based on customer profile.
    This is a simple implementation; more advanced logic can be added as needed.
    """

    # Example: If the customer is under 30, recommend Health insurance
    if customer.age < 30:
        recommended_policy = Policy.objects.filter(policy_type='Health').order_by('-premium').first()

    # Example: If the customer is between 30 and 60, recommend Life insurance
    elif 30 <= customer.age < 60:
        recommended_policy = Policy.objects.filter(policy_type='Life').order_by('-premium').first()

    # Example: If the customer is 60 or older, recommend more comprehensive Health insurance or Life insurance
    else:
        recommended_policy = Policy.objects.filter(policy_type='Health').order_by('-premium').first()

    # Return the most appropriate policy (or a list of policies if needed)
    return recommended_policy

def recommend_policies_for_multiple_customers():
    """
    Generate policy recommendations for multiple customers.
    This function returns a dictionary with customer names and their recommended policies.
    """
    customers = Customer.objects.all()
    recommendations = {}

    for customer in customers:
        recommended_policy = recommend_policy_for_customer(customer)
        recommendations[customer.name] = recommended_policy

    return recommendations
