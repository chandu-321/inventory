# inventory/urls.py
from django.urls import path

from .InventoryView import InventoryView
from .UserViews import UserRegistrationView, UserLoginView  # Import your views
from .ProtectedView import ProtectedView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('', InventoryView.as_view(), name='create_inventory'),  # POST for creation
    path('<int:id>/', InventoryView.as_view(), name='inventory_detail_update_delete'),  # GET, PUT, DELETE for item by ID
    path('get/', ProtectedView.as_view())
]
