from django.contrib import admin

from .models import BusinessProfile, PersonalProfile, User

admin.site.register(User)
admin.site.register(PersonalProfile)
admin.site.register(BusinessProfile)