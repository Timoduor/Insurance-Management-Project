from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User, Policy, Claim, InsurancePlan, Payment, Customer, Agent, Transaction
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'

class ClaimSerializer(serializers.ModelSerializer):
    policy_details = PolicySerializer(source='policy', read_only=True)

    class Meta:
        model = Claim
        fields = '__all__'

    def validate_amount(self, value):
        """Ensure claim amount is within policy limits"""
        policy = self.instance.policy if self.instance else None
        if policy and value > policy.coverage_amount:
            raise serializers.ValidationError("Claim amount exceeds policy coverage.")
        return value

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class InsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePlan
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'



User = get_user_model()

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation', 'phone_number', 'address', 'date_of_birth']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        user = User.objects.create_user(**validated_data)
        return user


# User Login Serializer (JWT token generation)
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        # Create JWT token
        access_token = str(RefreshToken.for_user(user).access_token)
        return {
            "user": user,
            "access_token": access_token
        }

# Policy Recommendation Serializer
class PolicyRecommendationSerializer(serializers.Serializer):
    """
    Serializer for a single policy recommendation.
    """
    policy_id = serializers.IntegerField(source='id')
    policy_type = serializers.CharField()
    coverage_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    premium = serializers.DecimalField(max_digits=10, decimal_places=2)

class CustomerPolicyRecommendationSerializer(serializers.Serializer):
    """
    Serializer for multiple customer policy recommendations.
    """
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField(source="name")
    recommended_policy = PolicyRecommendationSerializer()

# Analytics Serializers
class AnalyticsSerializer(serializers.Serializer):
    """
    Serializer for the overall insurance system analytics.
    """
    policy_stats = serializers.DictField(child=serializers.IntegerField())
    claim_stats = serializers.DictField(child=serializers.IntegerField())
    payment_stats = serializers.DictField(child=serializers.DecimalField(max_digits=15, decimal_places=2))

    # New additions for enhanced analytics
    total_customers = serializers.IntegerField()
    active_customers = serializers.IntegerField()
    average_transaction_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    fraud_statistics = serializers.DictField(child=serializers.IntegerField(), required=False)  # Placeholder for fraud detection


class CustomerClaimStatisticsSerializer(serializers.Serializer):
    """
    Serializer for claims per customer, including total claimed amount.
    """
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField(source="name")
    num_claims = serializers.IntegerField()
    total_claim_amount = serializers.DecimalField(max_digits=15, decimal_places=2)

class ClaimsByPolicyTypeSerializer(serializers.Serializer):
    """
    Serializer for claims grouped by policy type, including total payout.
    """
    policy_type = serializers.CharField(source="policy__policy_type")
    total_claims = serializers.IntegerField()
    total_payout = serializers.DecimalField(max_digits=15, decimal_places=2)
