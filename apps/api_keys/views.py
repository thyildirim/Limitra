from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.api_keys.models import ApiKey
from apps.api_keys.serializers import ApiKeySerializer
from apps.projects.models import Project


class ApiKeyListCreateView(generics.ListCreateAPIView): # list and create API view for API keys
    serializer_class = ApiKeySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ApiKey.objects.filter(
            project_id = self.kwargs["project_id"],
            project__owner=self.request.user
        )

    def perform_create(self, serializer):
        project = get_object_or_404(
            Project,
            id=self.kwargs["project_id"],
            owner=self.request.user
        )

        serializer.save(
            project=project,
            key = ApiKey.generate_key()
        )


class ApiKeyDetailView(generics.RetrieveUpdateDestroyAPIView): # retrieve, update, and delete API view for API keys
    serializer_class = ApiKeySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ApiKey.objects.filter(
            project__owner=self.request.user
        )