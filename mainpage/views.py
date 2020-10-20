from django.views.decorators.csrf import requires_csrf_token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import time
from . jenkinsTrigger import JenkinsTrigger

import asyncio
#SERVER_URL = "http://127.0.0.1:8000"
SERVER_URL = "http://3.137.149.140:8000"


class FileView(APIView):

    def get(self, request):
        return render(request, 'mainpage/index.html')

    def post(self, request):
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()

            import socket
            print(socket.gethostbyname(socket.getfqdn()))

            # Сheck the existence of the same file and delete it
            print("files/" + myfile.name)
            if (fs.exists("files/" + myfile.name) == True):
                fs.delete("files/" + myfile.name)

            if (fs.exists("files/" + myfile.name.split('.', 1)[0] + "_0001.png") == True):
                fs.delete("files/" + myfile.name.split('.', 1)[0] + "_0001.png")

            filename = fs.save("files/" + myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            # Activate the trigger
            trigger(uploaded_file_url)

            rendered_file_url = "files/" + \
                myfile.name.split('.', 1)[0] + "_0001.png"

            while (fs.exists(rendered_file_url) == False):
                time.sleep(1)

            return render(request, 'mainpage/index.html', {
                'rendered_file_url': rendered_file_url
            })
        return render(request, 'mainpage/index.html')


def trigger(url):
    NAME_OF_JOB = "get_data"
    TOKEN_NAME = "render"
    PARAMETERS = {'URL_FILE': SERVER_URL + url, }
    jenkins_obj = JenkinsTrigger()
    return asyncio.run(jenkins_obj.build_job(NAME_OF_JOB, PARAMETERS, TOKEN_NAME))


@api_view(['GET', 'POST', ])
@csrf_exempt
def ret(request):
    if request.method == 'POST' and request.FILES['upload_file']:
        myfile = request.FILES['upload_file']
        fs = FileSystemStorage()
        fs.save("files/" + myfile.name, myfile)
        return Response("Success")
    return Response("Error")


# Create your views here.
