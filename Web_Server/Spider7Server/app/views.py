from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json
# Create your views here.
@csrf_exempt
def my_api(requests):
    dic = {}
    if requests.method == "GET":
        dic['message'] = 0

    else:
        dic['message'] = '方法错误'


