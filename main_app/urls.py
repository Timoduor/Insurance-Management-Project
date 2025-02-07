from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, PolicyViewSet, ClaimViewSet, InsurancePlanViewSet, 
    PaymentViewSet, CustomerViewSet, AgentViewSet, TransactionViewSet, 
    index, about
)

# Registering ViewSets with DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'policies', PolicyViewSet)
router.register(r'claims', ClaimViewSet)
router.register(r'insuranceplans', InsurancePlanViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('api/', include(router.urls)),
]
