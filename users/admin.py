from django.contrib import admin
from .models import AccessToken

@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at", "expires_at")
    list_filter = ("created_at", "expires_at")
    search_fields = ("user__username", "token")
    readonly_fields = ("created_at",)