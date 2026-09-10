from rest_framework import serializers
from apps.api_keys.models import ApiKeys

class ApiKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKeys
        fields = [
            'id',
            'name',
            'key',
            'is_active',
            'created_at',
            'last_used_at',
        ]

        read_only_fields = [
            'id',
            'key',
            'created_at',
            'last_used_at',
        ]