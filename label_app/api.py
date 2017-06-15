from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
import os
from django.shortcuts import render, HttpResponse

from label_app.models import LogoCategory
from label_app.models import Photo
from label_app.models import UserLogoRelation
from label_app.models import LabelPosition
from label_app.models import VerifyStatus
from django.contrib.auth.models import User
import json
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
import datetime


class LogoCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LogoCategory
        fields = '__all__'
        depth = 1


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


class VerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = VerifyStatus
        fields = '__all__'


@api_view(['GET', 'POST','PUT'])
def logo_category(request, username=None):
    if request.method == 'GET':
        if username:
            logo_cate_list = LogoCategory.objects.filter(userlogorelation__user__username=username)
        else:
            logo_cate_list = LogoCategory.objects.all()
        serializer = LogoCategorySerializer(logo_cate_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #print(request.data)

        request.data['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        img_file = request.FILES.get('image')
        request.data['logo_category'] = os.path.splitext(img_file.name)[0]
        serializer = LogoCategorySerializer(data=request.data)
        serializer.validated_data.set('create_date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        cur_logo_cate = request.data['cur_logo_cate']
        l = LogoCategory.objects.filter(logo_category=cur_logo_cate)[0]
        new_logo_cate = request.data['new_logo_cate']
        l.logo_category = new_logo_cate
        l.save()
        ret_dict = {'logo_category': l.logo_category}
        return HttpResponse(json.dumps(ret_dict))


@api_view(['GET', 'POST', 'PUT'])
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
        logo_name = request.data['logo_category']
        request.data['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.data['logo_category'] = LogoCategory.objects.filter(logo_category=logo_name)
        print(request.data)
        img_file = request.FILES.get('image')
        ph = Photo.objects.filter(image='logo_pic/'+img_file.name)
        if ph:
            ret = {'ret': 'failed', 'msg': 'already exist'}
            return HttpResponse(json.dumps(ret), status=status.HTTP_201_CREATED)
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
            ret = {'ret': 'success', 'msg': 'add image success'}
            return HttpResponse(json.dumps(ret), status=status.HTTP_201_CREAT)
        ret = {'ret': 'failed', 'msg': 'bad request'}
        return HttpResponse(json.dumps(ret), status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'DELETE'])
def label_position(request, logo_cate=None, image_name=None):
    if request.method == 'GET':
        if image_name and logo_cate:
            label_pos_list = LabelPosition.objects.filter(photo__image='logo_pic/'+image_name)
        else:
            label_pos_list = LabelPosition.objects.all()

        #serializer = LabelPosSerializer(label_pos_list, many=True)
        #return Response(serializer.data, status=status.HTTP_201_CREATED)
        res_list = []
        for label in label_pos_list:
            ret_dict = {'label_user': label.label_user.username, 'label_name': label.label_name.logo_category,
                        'pos': label.pos, 'create_date': label.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'photo': label.photo.image.name}
            res_list.append(ret_dict)
        return HttpResponse(json.dumps(res_list))

    elif request.method == 'POST':
        if image_name and logo_cate:
            photos = Photo.objects.filter(image='logo_pic/' + image_name)
            if len(photos) > 0:
                photo = photos[0]
                #create_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                pos = request.data['pos']
                user = User.objects.filter(username=request.data['label_user'])[0]
                logo_name = LogoCategory.objects.filter(logo_category=logo_cate)[0]
                new_label = LabelPosition.objects.create(photo=photo,pos=pos, label_user=user,label_name=logo_name)
                new_label.save()
                res_data = {'username': user.username, 'image_name': image_name, 'logo_cate': logo_cate}
                return HttpResponse(json.dumps(res_data), status=status.HTTP_201_CREATED)
            else:
                res_data = {'ret': False, 'msg': 'image not exist'}
                return HttpResponse(json.dumps(res_data), status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if image_name:
            label_pos_list = LabelPosition.objects.filter(photo__image='logo_pic/' + image_name)
            label_pos_list.delete()
            res_data = {'image_name': image_name}
            return HttpResponse(json.dumps(res_data), status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def verify_status(request, logo_cate=None, image_name=None):
    if request.method == 'GET':
        if image_name and logo_cate:
            verify_list = VerifyStatus.objects.filter(photo__image='logo_pic/'+logo_cate+'/'+image_name)
        else:
            verify_list = VerifyStatus.objects.all()
        serializer = VerifySerializer(verify_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if image_name and logo_cate:
            verify_list = VerifyStatus.objects.filter(photo__image='logo_pic/'+logo_cate+'/'+image_name)
            user = User.objects.filter(username=request.data['verify_people'])[0]
            if len(verify_list) > 0:
                for v in verify_list:
                    v.isVerify = request.data['isVerify']
                    v.verify_people = user
                    v.save()
                    res_data = {'verify_people': user.username, 'isVerify': v.isVerify}
                    return HttpResponse(json.dumps(res_data), status=status.HTTP_201_CREATED)
            else:
                photo = Photo.objects.filter(image='logo_pic/' + logo_cate + '/' + image_name)[0]
                v = VerifyStatus.objects.create(isVerify=request.data['isVerify'], verify_people=user, photo=photo)
                v.save()
                res_data = {'verify_people': user.username, 'isVerify': v.isVerify}
                return HttpResponse(json.dumps(res_data), status=status.HTTP_201_CREATED)



