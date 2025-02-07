from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Policy, Claim, InsurancePlan, Payment, Customer, Agent, Transaction
from .serializers import (
    UserSerializer, PolicySerializer, ClaimSerializer, 
    InsurancePlanSerializer, PaymentSerializer, CustomerSerializer, 
    AgentSerializer, TransactionSerializer
)

# Home & Static Pages
def index(request):
    return JsonResponse({"message": "Welcome to the Insurance Portal API"})

def about(request):
    return JsonResponse({"message": "This is an insurance management system"})

# ViewSets for each model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def create(self, request, *args, **kwargs):
        policy_id = request.data.get('policy')
        claim_amount = float(request.data.get('amount', 0))

        policy = get_object_or_404(Policy, id=policy_id)
        if policy.start_date <= timezone.now().date() <= policy.end_date:
            if claim_amount <= policy.coverage_amount:
                return super().create(request, *args, **kwargs)
            return Response({'error': 'Claim amount exceeds policy coverage'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Policy is not active'}, status=status.HTTP_400_BAD_REQUEST)

class InsurancePlanViewSet(viewsets.ModelViewSet):
    queryset = InsurancePlan.objects.all()
    serializer_class = InsurancePlanSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
