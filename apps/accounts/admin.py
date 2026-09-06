from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('id',)
