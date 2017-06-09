from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate
import json


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

