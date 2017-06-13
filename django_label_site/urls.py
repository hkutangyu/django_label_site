"""django_label_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from label_app.views import api_auth
from label_app.views import upload_logo_samples
from label_app.views import upload_logo_sample
from label_app.api import logo_category
from label_app.api import logo_images
from label_app.api import label_position

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api_auth/', api_auth),
    url(r'upload_logo_samples/', upload_logo_samples),
    url(r'upload_logo_sample/', upload_logo_sample),
    url(r'api/logo_categories/$', logo_category, name='logo_categories'),
    url(r'api/logo_categories/(?P<username>[A-Za-z]+)$', logo_category, name='logo_categories'),
    url(r'api/logo_images/$', logo_images, name='logo_images'),
    url(r'api/logo_images/(?P<logo_cate>.+)$', logo_images, name='logo_images'),
    url(r'api/label_position/$', label_position),
    url(r'api/label_position/(?P<logo_cate>.+)/(?P<image_name>.+)$', label_position)
]
