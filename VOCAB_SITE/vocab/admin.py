from django.contrib import admin
from .models import UserProfile, RegisteredIRI

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RegisteredIRI)