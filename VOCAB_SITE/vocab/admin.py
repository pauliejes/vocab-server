from django.contrib import admin
from .models import UserProfile, RegisteredIRI, Vocabulary, Term

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RegisteredIRI)
admin.site.register(Vocabulary)
admin.site.register(Term)
