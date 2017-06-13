from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
import os

from label_app.models import LogoCategory
from label_app.models import Photo
from label_app.models import UserLogoRelation
from label_app.models import LabelPosition
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import datetime


class LogoCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LogoCategory
        fields = '__all__'


class LogoImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'

class UserLogoRSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLogoRelation
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'


class LabelPosSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabelPosition
        fields = '__all__'

@api_view(['GET', 'POST'])
def logo_category(request, username=None):
    if request.method == 'GET':
        if username:
            logo_cate_list = LogoCategory.objects.filter(userlogorelation__user__username=username)

        else:
            logo_cate_list = LogoCategory.objects.all()
        serializer = LogoCategorySerializer(logo_cate_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        request.data['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        img_file = request.FILES.get('image')
        request.data['logo_category'] = os.path.splitext(img_file.name)[0]
        print(request.data)
        serializer = LogoCategorySerializer(data=request.data)
        #serializer.validated_data.set('create_date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def logo_images(request, logo_cate=None):
    if request.method == 'GET':
        if logo_cate:
            logo_images_list = Photo.objects.filter(logo_category__logo_category=logo_cate)
        else:
            logo_images_list = Photo.objects.all()
        serializer = LogoImagesSerializer(logo_images_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(request.data)
        logo_cate = request.data['logo_category']
        request.data['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.data['isVerify'] = False
        request.data['verify_people'] = User.objects.filter(username='admin')
        request.data['logo_category'] = LogoCategory.objects.filter(logo_category=logo_cate)
        print(request.data)
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def label_position(request, logo_cate=None, image_name=None):
    if request.method == 'GET':
        if image_name and logo_cate:
            label_pos_list = LabelPosition.objects.filter(photo__image='logo_pic/'+logo_cate+'/'+image_name)

            serializer = LabelPosSerializer(label_pos_list, many=True)
            return Response(serializer.data)
        else:
            label_pos_list = LabelPosition.objects.all()
            serializer = LabelPosSerializer(label_pos_list, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
