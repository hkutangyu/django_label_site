from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class LogoCategory(models.Model):
    logo_category = models.CharField(max_length=50, null=False)
    create_date = models.DateField()

    def __str__(self):
        return self.logo_category


class UserLogoRelation(models.Model):
    user = models.ForeignKey(User)
    logo_category = models.ManyToManyField(LogoCategory)
    create_date = models.DateField()



