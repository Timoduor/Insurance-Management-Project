from django.contrib import admin
from .models import User, Customer, Agent, Policy, Claim, InsurancePlan, Payment, Transaction

# UserAdmin with custom fields
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'gender', 'role', 'is_active', 'is_staff', 'date_of_birth', 'profile_picture')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('role', 'is_active', 'is_staff', 'gender')
    
    # Allow filtering by role and viewing custom fields
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'phone_number', 'gender', 'date_of_birth', 'profile_picture', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

# CustomerAdmin with basic customer details
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address')  
    search_fields = ('name', 'email', 'phone_number')  

# AgentAdmin for managing agents
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'agency')
    search_fields = ('name', 'email', 'phone')

# PolicyAdmin with key details about policies
@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_number', 'policy_type', 'user', 'coverage_amount', 'premium', 'status')
    search_fields = ('policy_number', 'user__username', 'policy_type')
    list_filter = ('policy_type', 'status', 'start_date', 'end_date')

# ClaimAdmin for managing claims related to policies
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_number', 'policy', 'claim_date', 'amount', 'status')
    search_fields = ('claim_number', 'policy__policy_number')
    list_filter = ('status', 'claim_date')

# InsurancePlanAdmin for different insurance plans
@admin.register(InsurancePlan)
class InsurancePlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'coverage_amount', 'monthly_premium')
    search_fields = ('plan_name',)

# PaymentAdmin to manage payments made for policies
# PaymentAdmin to display and manage Payment objects in the admin interface
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('policy', 'payment_date', 'amount', 'transaction_type')  # Corrected field name
    search_fields = ('policy__policy_number', 'transaction_type')  # Corrected field name
    list_filter = ('payment_date', 'transaction_type')  # Corrected field name

# TransactionAdmin to keep track of transactions between customer and policy
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'policy', 'amount', 'date')
    search_fields = ('customer__name', 'policy__policy_number')
    list_filter = ('date',)