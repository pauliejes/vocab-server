from django.contrib import admin
from .models import UserProfile, RegisteredIRI, VocabularyData, TermTypeData, TermData

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(RegisteredIRI)
admin.site.register(VocabularyData)
admin.site.register(TermTypeData)
admin.site.register(TermData)