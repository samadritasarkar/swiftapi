from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
import requests, os
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from .models import Object
from .forms import ObjectForm
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView


class ContainerList(APIView):

    def generate_token(request, format=None):
        url = 'http://10.129.103.86:5000/v3/auth/tokens'
        headers = {'content-type': 'application/json'}
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        r = requests.post(url, headers=headers, data=data)
        headers = r.headers.get('X-Subject-Token')
        return headers

    def get(self, request, format=None):
        token = self.generate_token(request)
        r = requests.get('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/',
                         headers={'X-Auth-Token': token}).text
        obj_arr = r.split("\n")
        obj_arr.pop()
        rows = len(obj_arr)
        columns = 3
        Matrix = [[0 for x in range(columns)] for x in range(rows)]
        for i in range(rows):
            Matrix[i][0] = obj_arr[i]
            Matrix[i][1] = reverse('files:cont_info', kwargs={'container': obj_arr[i]}, request=request, format=format)
            Matrix[i][2] = reverse('files:upload', kwargs={'container': obj_arr[i]}, request=request, format=format)
        return Response(Matrix)

    def put(self, request, format=None):
        data = JSONParser().parse(request)
        new_cont = data["name"]
        r = requests.put('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + new_cont,
                         headers={'X-Auth-Token': token}).text
        return Response(r)


class ObjectList(APIView):

    def generate_token(request, format=None):
        url = 'http://10.129.103.86:5000/v3/auth/tokens'
        headers = {'content-type': 'application/json'}
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        r = requests.post(url, headers=headers, data=data)
        headers = r.headers.get('X-Subject-Token')
        return headers

    def get(self, request,container, format=None):
        token = self.generate_token(request)
        r = requests.get('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container,
                         headers={'X-Auth-Token': token}).text

        obj_arr = r.split("\n")
        obj_arr.pop()
        rows = len(obj_arr)
        columns = 3
        Matrix = [[0 for x in range(columns)] for x in range(rows)]
        for i in range(rows):
            Matrix[i][0] = obj_arr[i]
            Matrix[i][1] = reverse('files:obj_info', kwargs={'container': container, 'object': obj_arr[i]},
                                   request=request, format=format)
            Matrix[i][2] = reverse('files:obj_download', kwargs={'container': container, 'object': obj_arr[i]},
                                   request=request, format=format)
        return Response(Matrix)

    def delete(self,request,container, format=None):
        token = self.generate_token(request)
        r = requests.delete('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container,
                            headers={'X-Auth-Token': token}).text
        return Response(r)

    def post(self,request,container, format=None):
        token = self.generate_token(request)
        data = JSONParser().parse(request)
        data.update(t)
        requests.post('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container, headers=data)
        r = requests.get('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container,
                         headers={'X-Auth-Token': token})
        return Response(r.headers)


class DownloadObject(APIView):

    def generate_token(request, format=None):
        url = 'http://10.129.103.86:5000/v3/auth/tokens'
        headers = {'content-type': 'application/json'}
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        r = requests.post(url, headers=headers, data=data)
        headers = r.headers.get('X-Subject-Token')
        return headers

    def get(self, request,container,object, format=None):

        token = self.generate_token(request)
        r = requests.get(
            'http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
            headers={'X-Auth-Token': token})

        name, ext = os.path.splitext(object)
        if (ext == ".png"):
            return HttpResponse(r, 'image/png')
        elif (ext == ".jpeg"):
            return HttpResponse(r, 'image/jpeg')
        elif (ext == ".txt"):
            return HttpResponse(r, 'text/plain')
        elif (ext == ".pdf"):
            return HttpResponse(r, 'application/pdf')
        elif (ext == ".zip"):
            return HttpResponse(r, 'application/zip')
        elif (ext == ".mp4"):
            return HttpResponse(r, 'audio/mp4')
        elif (ext == ".mp3"):
            return HttpResponse(r, 'audio/basic')
        else:
            return Response("Format Not Supported!")

class ObjectDetails(APIView):

    def generate_token(request, format=None):
        url = 'http://10.129.103.86:5000/v3/auth/tokens'
        headers = {'content-type': 'application/json'}
        data = '\n{ "auth": {\n    "identity": {\n      "methods": ["password"],\n      "password": {\n        "user": {\n          "name": "swift",\n          "domain": { "name": "default" },\n          "password": "swift"\n        }\n      }\n    },\n    "scope": {\n      "project": {\n        "name": "service",\n        "domain": { "name": "default" }\n      }\n    }\n  }\n}'
        r = requests.post(url, headers=headers, data=data)
        headers = r.headers.get('X-Subject-Token')
        return headers

    def get(self, request,container,object, format=None):
        token = self.generate_token(request)
        r = requests.get(
            'http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
            headers={'X-Auth-Token': token})
        return Response(r.headers)

    def post(self, request,container,object, format=None):
        token = self.generate_token(request)
        t = {'X-Auth-Token': token}
        data = JSONParser().parse(request)
        data.update(t)
        requests.post('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
                      headers=data)
        r = requests.get(
            'http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
            headers={'X-Auth-Token': token})
        return Response(r.headers)

    def delete(self, request, container, object, format=None):
        token = self.generate_token(request)
        r = requests.delete(
            'http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
            headers={'X-Auth-Token': token}).text
        return Response(r)

@api_view(['GET', 'DELETE', 'POST'])
def object_details (request, container, object, format=None):
    token = ObjectList.generate_token(request)

    if request.method == 'GET':
        r = requests.get('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
            headers={'X-Auth-Token': token})
        return Response (r.headers)
    if request.method == 'POST':
        t = {'X-Auth-Token': token}
        data = JSONParser().parse(request)
        data.update(t)
        requests.post('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
                      headers=data)
        r = requests.get(
            'http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
            headers={'X-Auth-Token': token})
        return Response(r.headers)

    if request.method == 'DELETE':
        r = requests.delete(
            'http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + object,
            headers={'X-Auth-Token': token}).text
        return Response(r)



@api_view (['GET', 'POST'])
def upload(request, container, format=None):
    form = ObjectForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        a = form.save(commit=False)
        a.file = request.FILES['file']
        name, ext = os.path.splitext(a.file.name)
        if (ext == ".png" or ext == ".jpeg" or ext == ".mp4" or ext == ".mp3" or ext == ".pdf" or ext == ".zip" or ext == ".txt"):
            a.save()
            token = ObjectList.generate_token(request)
            path = "C:/Users/Samadrita/Desktop/swift1/media/"+a.file.name
            s = requests.put('http://10.129.103.86:8080/v1/AUTH_b3f70be8acad4ec197e2b5edf48d9e5a/' + container + '/' + a.file.name,
                             headers={'X-Auth-Token': token}, data=open(path, "rb")).text
            os.remove(path)
            return Response(s)
        else:
            return Response("Format not supported. Supported formats include png, jpeg, mp3, mp4, zip, pdf, txt. For all other files, create a zip file and try again!")
    context = {
        "form": form,
    }
    return render(request, 'files/input.html', context)


