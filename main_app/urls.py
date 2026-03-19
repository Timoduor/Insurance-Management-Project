from django.urls import include, path 
from rest_framework.routers import DefaultRouter
from .views import(
    UserViewSet, PolicyViewSet, ClaimViewSet, InsurancePlanViewSet,
    PaymentViewSet, CustomerViewSet, AgentViewSet, TransactionViewSet, UserRegistrationView, UserLoginView,
    index, about, customer_form, agent_form, transaction_form, AnalyticsView, PolicyRecommendationView,
)
from oauth2_provider.views import TokenView, AuthorizeView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'policies', PolicyViewSet, basename='policy')
router.register(r'claims', ClaimViewSet, basename='claim')
router.register(r'insuranceplans', InsurancePlanViewSet, basename='insuranceplan')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('', include(router.urls)),  # API endpoints
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('recommendations/', PolicyRecommendationView.as_view(), name='policy-recommendations'),
    path('recommendations/<int:customer_id>/', PolicyRecommendationView.as_view(), name='policy-recommendations-single'),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # OAuth2 routes
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # OAuth2 routes
    path('o/token/', TokenView.as_view(), name='token'),
    path('o/authorize/', AuthorizeView.as_view(), name='authorize'),

    #  Form-based Views
    path('customers/new/', customer_form, name='customer_form'),
    path('customers/edit/<int:id>/', customer_form, name='edit_customer'),
    
    path('agents/new/', agent_form, name='agent_form'),
    path('agents/edit/<int:id>/', agent_form, name='edit_agent'),
    
    path('transactions/new/', transaction_form, name='transaction_form'),
    path('transactions/edit/<int:id>/', transaction_form, name='edit_transaction'),
]
