from django.urls import path
from .views import ApiKeyListCreateView, ApiKeyDetailView

urlpatterns = [
    path('projects/<int:project_id>/api-keys/', ApiKeyListCreateView.as_view(), name='api_key_list_create'),
    path('api-keys/<int:pk>/', ApiKeyDetailView.as_view(),name='api_key_detail'),
]