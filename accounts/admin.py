from django.contrib import admin

from .models import BusinessProfile, User, UserProfile

admin.site.register(UserProfile)
admin.site.register(BusinessProfile)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_active")
    ordering = ("email",)
    search_fields = ("email",)