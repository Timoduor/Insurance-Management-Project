from django.contrib import admin
from django.urls import include, path 
from rest_framework.routers import DefaultRouter
from main_app.views import (
    UserViewSet, PolicyViewSet, ClaimViewSet, InsurancePlanViewSet, 
    PaymentViewSet, CustomerViewSet, AgentViewSet, TransactionViewSet,
    index, about
)


# Initialize DefaultRouter and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'policies', PolicyViewSet)
router.register(r'claims', ClaimViewSet)
router.register(r'insuranceplans', InsurancePlanViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'customers', CustomerViewSet)  # Ensure this is registered
router.register(r'agents', AgentViewSet)
router.register(r'transactions', TransactionViewSet)

# Define urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # Homepage API response
    path('about/', about, name='about'),  # About API response
    path('auth/', include('djoser.urls')),  # Authentication endpoints
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),  # Include app URL at the root
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

