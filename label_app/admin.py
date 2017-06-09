from django.contrib import admin
from label_app.models import LogoCategory
from label_app.models import UserLogoRelation

# Register your models here.
admin.site.register(LogoCategory)
admin.site.register(UserLogoRelation)


