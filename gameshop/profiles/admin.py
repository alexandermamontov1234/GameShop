from django.contrib import admin
from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("first_name", 'last_name')}


admin.site.register(Profile, ProfileAdmin)
