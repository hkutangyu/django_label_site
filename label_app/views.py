# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import os
import shutil

LOGO_SAMPLES_FOLDER = '/home/tangyu/logo_db/logo_samples/'

# Create your views here.
def api_auth(request):
    if request.method == 'POST':
        print('POST coming')
        return HttpResponse('POST')
    else:
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=username, password=password)
        ret_json = {}
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            ret_json['auth_status'] = True
            return HttpResponse(json.dumps(ret_json, ensure_ascii=False))
        else:
            # Show an error page
            ret_json['auth_status'] = False
            return HttpResponse(json.dumps(ret_json, ensure_ascii=False))


@csrf_exempt
def upload_logo_samples(request):
    ret_dict = {}
    if request.method == 'POST':
        zipfile = request.FILES.get('file')
        print(zipfile.name)
        file_full_path = os.path.join(LOGO_SAMPLES_FOLDER, zipfile.name)
        destination = open(file_full_path, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in zipfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # uncompress
        unzip_cmd = 'unzip -o -O CP936 ' + file_full_path + ' -d ' + LOGO_SAMPLES_FOLDER
        os.system(unzip_cmd)
        os.remove(file_full_path)
        ret_dict['ret'] = True
        ret_dict['msg'] = 'upload ok'
        return HttpResponse(json.dumps(ret_dict, ensure_ascii=False))
    else:
        ret_dict['ret'] = False
        ret_dict['msg'] = 'Please user POST method'
        return HttpResponse(json.dumps(ret_dict))

