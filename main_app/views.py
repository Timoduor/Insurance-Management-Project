from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView # Part of the analytics view
from .policy_recommendation import recommend_policy_for_customer, recommend_policies_for_multiple_customers
from .models import (
    User, Policy, Claim, InsurancePlan, Payment, 
    Customer, Agent, Transaction
)
from .serializers import (
    UserSerializer, PolicySerializer, ClaimSerializer, AnalyticsSerializer,
    InsurancePlanSerializer, PaymentSerializer, CustomerSerializer, 
    AgentSerializer, TransactionSerializer, UserRegistrationSerializer, UserLoginSerializer, CustomerClaimStatisticsSerializer, ClaimsByPolicyTypeSerializer, CustomerPolicyRecommendationSerializer
)
from .forms import CustomerForm, AgentForm, TransactionForm
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .fraud_detection import detect_fraud  # Import the fraud detection function
from .analytics import get_analytics_summary, get_policy_statistics, get_claim_statistics, get_payment_statistics, get_customer_claim_statistics, get_claims_by_policy_type # Import the analytics functions
from django.db.models import Sum, Count  # Add missing import
from django.core.exceptions import ObjectDoesNotExist
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.views import TokenView
from rest_framework.exceptions import AuthenticationFailed
from oauth2_provider.models import AccessToken
from django_ratelimit.decorators import ratelimit


# 🌟 API Root View with JSON & HTML Support
def index(request):
    if request.headers.get("Accept") == "application/json":
        return JsonResponse({
            "message": "Welcome to the Insurance Portal API",
            "status": "success",
            "endpoints": {
                "users": "/users/",
                "customers": "/customers/",
                "policies": "/policies/",
                "claims": "/claims/",
                "insurance plans": "/insuranceplans/",
                "payments": "/payments/",
                "agents": "/agents/",
                "transactions": "/transactions/",
                "authentication": {
                    "register": "/auth/users/",
                    "login": "/auth/token/login/",
                    "logout": "/auth/token/logout/"
                }
            }
        }, json_dumps_params={'indent': 4})

    return render(request, "main_app/index.html")

# 🌟 About Page View
def about(request):
    return render(request, "main_app/about.html")

# 🌟 User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 🌟 Policy ViewSet
class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

# 🌟 Claim ViewSet with Policy Validation
class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def create(self, request, *args, **kwargs):
        policy_id = request.data.get('policy')
        claim_amount = float(request.data.get('amount', 0))

        policy = get_object_or_404(Policy, id=policy_id)
        current_date = timezone.now().date()

        if policy.start_date <= current_date <= policy.end_date:
            if claim_amount <= policy.coverage_amount:
                return super().create(request, *args, **kwargs)
            return Response({'error': 'Claim amount exceeds policy coverage'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'Policy is not active'}, status=status.HTTP_400_BAD_REQUEST)
    
        customer_id = request.data.get('customer')  # Assuming 'customer' is provided in the request data
        customer = Customer.objects.get(id=customer_id)
        
        # Check if the customer is involved in fraud
        if detect_fraud(customer):
            return Response({"error": "Fraud detected!"}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating the claim if no fraud detected
        return super().create(request, *args, **kwargs)

# 🌟 Insurance Plan ViewSet
class InsurancePlanViewSet(viewsets.ModelViewSet):
    queryset = InsurancePlan.objects.all()
    serializer_class = InsurancePlanSerializer

# 🌟 Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# 🌟 Customer ViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# 🌟 Agent ViewSet
class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

# 🌟 Transaction ViewSet
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# 🌟 Customer Form View
def customer_form(request, id=None):
    customer = get_object_or_404(Customer, id=id) if id else None
    form = CustomerForm(instance=customer) if customer else CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customers/')

    return render(request, 'main_app/customer_form.html', {'form': form})

# 🌟 Agent Form View
def agent_form(request, id=None):
    agent = get_object_or_404(Agent, id=id) if id else None
    form = AgentForm(instance=agent) if agent else AgentForm()

    if request.method == 'POST':
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            return redirect('/agents/')

    return render(request, 'main_app/agent_form.html', {'form': form})

# 🌟 Transaction Form View
def transaction_form(request, id=None):
    transaction = get_object_or_404(Transaction, id=id) if id else None
    form = TransactionForm(instance=transaction) if transaction else TransactionForm()

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('/transactions/')

    return render(request, 'main_app/transaction_form.html', {'form': form})

# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login View (JWT Authentication)
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Generate JWT token on successful login
            access_token = serializer.validated_data['access_token']
            refresh_token = serializer.validated_data['refresh_token']
            
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# View requiring OAuth2 Authentication (Example)
class ProtectedView(APIView):
    authentication_classes = [OAuth2Authentication]  # Use OAuth2Authentication here
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get(self, request, *args, **kwargs):
        return Response({"message": "This is a protected view!"}, status=status.HTTP_200_OK)


# Custom error handling in the Tokenview
class CustomTokenView(TokenView):
    @ratelimit(key='ip', rate='5/m', method='ALL')
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except AuthenticationFailed as e:
            return Response({"error": "Invalid OAuth2 token or expired"}, status=status.HTTP_401_UNAUTHORIZED)
        return response


class AnalyticsView(APIView):
    """
    API view to get the overall analytics summary for the insurance system.
    """

    def get(self, request, *args, **kwargs):
        """
        Fetch overall analytics, including policy, claim, payment, and customer statistics.
        """

        analytics_summary = {
            'policy_stats': get_policy_statistics(),
            'claim_stats': get_claim_statistics(),
            'payment_stats': get_payment_statistics(),
            'total_customers': Customer.objects.count(),  # New Field
            'active_customers': Customer.objects.filter(status='Active').count(),  # New Field
            'average_transaction_amount': Payment.objects.aggregate(avg_amount=Sum('amount') / Count('id'))['avg_amount'] or 0  # New Field
        }

        serializer = AnalyticsSerializer(analytics_summary)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerClaimStatisticsView(APIView):
    """
    API view to get claim statistics per customer.
    """

    def get(self, request, *args, **kwargs):
        customer_claims = get_customer_claim_statistics()
        serializer = CustomerClaimStatisticsSerializer(customer_claims, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClaimsByPolicyTypeView(APIView):
    """
    API view to get claims grouped by policy type.
    """

    def get(self, request, *args, **kwargs):
        claims_by_policy = get_claims_by_policy_type()
        serializer = ClaimsByPolicyTypeSerializer(claims_by_policy, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PolicyRecommendationView(APIView):
    """
    API view to get policy recommendations for a specific customer or all customers.
    """

    def get(self, request, customer_id=None, *args, **kwargs):
        """
        If customer_id is provided, return a policy recommendation for that customer.
        Otherwise, return recommendations for all customers.
        """

        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                recommended_policy = recommend_policy_for_customer(customer)

                if recommended_policy:
                    data = {
                        'customer': customer.name,
                        'recommended_policy': recommended_policy.policy_type,
                        'coverage_amount': recommended_policy.coverage_amount,
                        'premium': recommended_policy.premium
                    }
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "No policy found for recommendation."}, status=status.HTTP_404_NOT_FOUND)

            except ObjectDoesNotExist:
                return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        else:
            recommendations = recommend_policies_for_multiple_customers()
            serializer = CustomerPolicyRecommendationSerializer(recommendations.values(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)