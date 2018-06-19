from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import FileUploadParser
from .models import Container, Objects
from rest_framework.views import APIView
from .forms import ObjectForm
import requests, re, json


class ContainerList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'files/display_cont.html'

    def generate_token(request, format=None):
        url = 'http://10.129.103.86:5000/v3/auth/tokens'
        headers = {'content-type': 'application/json'}
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        r = requests.post(url, headers=headers, data=data)
        headers = r.headers.get('X-Subject-Token')
        return headers

    def get(self, request, format=None):
        token = self.generate_token(request)
        r = requests.get('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/', headers={'X-Auth-Token': token}).text
        obj_arr = r.split("\n")
        obj_arr.pop()

        return Response({'obj_arr':obj_arr})


class ObjectList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'files/display_objects.html'

    def generate_token(request, format=None):
        url = 'http://10.129.103.86:5000/v3/auth/tokens'
        headers = {'content-type': 'application/json'}
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        r = requests.post(url, headers=headers, data=data)
        headers = r.headers.get('X-Subject-Token')
        return headers

    def get(self, request,container, format=None):
        token = self.generate_token(request)
        r = requests.get('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/'+container,headers={'X-Auth-Token': token}).text
        obj_arr = r.split("\n")
        obj_arr.pop()

        return Response({'obj_arr':obj_arr, 'container':container})


@api_view(['GET'])
def download_object(request, container, object, format=None):

    token = ObjectList.generate_token(request)
    if request.method == 'GET':
        r = requests.get(
            'http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
            headers={'X-Auth-Token': token})

        with open(object, "wb") as code:
            code.write(r.content)
        return render(request, 'files/success.html')
