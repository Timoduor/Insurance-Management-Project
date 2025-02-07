from rest_framework import serializers
from .models import User, Policy, Claim, InsurancePlan, Payment, Customer, Agent, Transaction

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
