from django.urls import path
from .views import ProjectCreateView, ProjectListView, ProjectDetailView, ProjectUpdateView

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    ]