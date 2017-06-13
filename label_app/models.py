from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.core.validators import validate_comma_separated_integer_list
import os

# Create your models here.


class LogoCategory(models.Model):
    logo_category = models.CharField(verbose_name='商标名称', max_length=50, null=False, unique=True)
    image = models.ImageField(verbose_name='图片', null=True, upload_to='logo_samples')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_created=True)
    # 加入用户字段和分配时间？
    # user = models.ForeignKey(User, verbose_name='归属用户', null=True, blank=True)
    # create_date = models.DateField(verbose_name='分配时间', null=True, blank=True)

    def __str__(self):
        return self.logo_category

    class Meta:
        verbose_name = "商标类别"
        verbose_name_plural = "商标类别"


class UserLogoRelation(models.Model):
    user = models.ForeignKey(User, verbose_name='归属用户')
    logo_category = models.ManyToManyField(LogoCategory, verbose_name='商标名称')
    create_date = models.DateTimeField(verbose_name='分配时间', auto_now=True)

    class Meta:
        verbose_name = "商标分配"
        verbose_name_plural = "商标分配"

    def __str__(self):
        return self.logo_category.logo_category + '->' + self.user.username


def upload_to(instance, filename):
    return 'logo_pic/' + instance.logo_category.logo_category + '/' + filename


def delete_file(sender, **kwargs):
    patch = kwargs['instance']
    if os.path.exists(patch.image.path):
        os.remove(patch.image.path)


class Photo(models.Model):

    #name = models.CharField(verbose_name='文件名', max_length=100, null=False)
    logo_category = models.ForeignKey(LogoCategory, verbose_name='图片类别')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    image = models.ImageField(verbose_name='图片', null=False, upload_to=upload_to)

    def __str__(self):
        return self.image.name


class VerifyStatus(models.Model):
    isVerify = models.BooleanField(verbose_name='审核状态', default=False)
    verify_people = models.ForeignKey(User, verbose_name='审核人')
    photo = models.ForeignKey(Photo, verbose_name='图片')


class LabelPosition(models.Model):
    photo = models.ForeignKey(Photo, verbose_name='图片')
    create_date = models.DateTimeField(verbose_name='标注时间', auto_now=True)
    pos = models.CharField(max_length=100,
                           validators=[validate_comma_separated_integer_list],
                           verbose_name='标注坐标')
    label_user = models.ForeignKey(User, verbose_name='标注人')
    label_name = models.ForeignKey(LogoCategory, verbose_name='类别')


post_delete.connect(delete_file, sender=Photo)
post_delete.connect(delete_file, sender=LogoCategory)

