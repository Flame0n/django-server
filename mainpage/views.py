from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class FileView(APIView):

    def get(self, request):
        return render(request, 'mainpage/index.html')

    def post(self, request):
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save("files/" + myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(request, 'mainpage/index.html', {
                'uploaded_file_url': uploaded_file_url
            })
        return render(request, 'mainpage/index.html')



# Create your views here.
