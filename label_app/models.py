from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class LogoCategory(models.Model):
    logo_category = models.CharField(verbose_name='商标名称', max_length=50, null=False)
    image_field = models.ImageField(verbose_name='图片', null=False)
    create_date = models.DateField(verbose_name='创建时间')

    def __str__(self):
        return self.logo_category

    class Meta:
        verbose_name = "商标类别"
        verbose_name_plural = "商标类别"


class UserLogoRelation(models.Model):
    user = models.ForeignKey(User, verbose_name='归属用户')
    logo_category = models.ManyToManyField(LogoCategory, verbose_name='商标名称')
    create_date = models.DateField(verbose_name='创建时间')

    class Meta:
        verbose_name = "商标分配"
        verbose_name_plural = "商标分配"



