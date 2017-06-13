from django.contrib import admin
from label_app.models import LogoCategory
from label_app.models import UserLogoRelation
from label_app.models import Photo
from label_app.models import LabelPosition
from label_app.models import VerifyStatus

class PhotoAdmin(admin.ModelAdmin):
    verbose_name = '商标图片'
    list_display = ('logo_category', 'image')
    search_fields = ('logo_category__logo_category',)
    app_label = 'label_app'

# Register your models here.
admin.site.register(LogoCategory)
admin.site.register(UserLogoRelation)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(LabelPosition)
admin.site.register(VerifyStatus)


