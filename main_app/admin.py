from django.contrib import admin
from .models import User, Customer, Agent, Policy, Claim, InsurancePlan, Payment, Transaction

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_agent', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_agent', 'is_staff', 'is_active')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone')

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'agency')
    search_fields = ('name', 'email', 'phone')

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_number', 'policy_type', 'user', 'coverage_amount', 'premium', 'status')
    search_fields = ('policy_number', 'user__username', 'policy_type')
    list_filter = ('policy_type', 'status', 'start_date', 'end_date')

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_number', 'policy', 'claim_date', 'amount', 'status')
    search_fields = ('claim_number', 'policy__policy_number')
    list_filter = ('status', 'claim_date')

@admin.register(InsurancePlan)
class InsurancePlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'coverage_amount', 'monthly_premium')
    search_fields = ('plan_name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('policy', 'payment_date', 'amount', 'payment_method')
    search_fields = ('policy__policy_number', 'payment_method')
    list_filter = ('payment_date', 'payment_method')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'policy', 'amount', 'date')
    search_fields = ('customer__name', 'policy__policy_number')
    list_filter = ('date',)
