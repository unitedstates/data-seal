from django.shortcuts import render
from authentication.authapp.models import Document


def index(request):
  return render(request, template_name='authentication/index.html')

def upload(request):
  raise NotImplementedError

def search(request):
  raise NotImplementedError

def file_detail(request, file_slug):
  raise NotImplementedError

def file_download(request, file_slug):
  raise NotImplementedError

def file_signature(request, file_slug):
  raise NotImplementedError
