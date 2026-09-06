
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import Account


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']


    def create(self,validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance