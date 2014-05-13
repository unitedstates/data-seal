from django import forms
from django.shortcuts import get_object_or_404, render
from authentication.authapp.models import Document
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import json

def index(request):
    return render(request, 'authentication/index.html')

##########


class UploadForm(forms.Form):
    user_file = forms.FileField(label="File you want to check")

class LoginForm(forms.Form):
    Username = forms.CharField(max_length=50)
    Password = forms.CharField(max_length=50)

def upload(request):
    post = False
    form = None
    document = None
    validation = None

    if request.method == 'POST':
        post = True
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            documents = Document.find_user_file(request.FILES['user_file'])
            if documents:
                document = documents.first()
                validation = document.test_user_file(request.FILES['user_file'])
                return HttpResponse(json.dumps({'document': {"name":document.name, "sha512":document.sha512, "uploaded":str(document.uploaded)},'validation': {"is_valid":validation.valid, "fingerprint":validation.fingerprint}}), content_type = "application/json")
            else:
                return HttpResponse(json.dumps({'document': None,'validation': None}), content_type = "application/json")
    else:
        form = UploadForm()

    return render(request, 'authentication/upload.html', {
        'post': post,
        'form': form,
        'document': document,
        'validation': validation
    })

    

##########


def search(request):
    raise NotImplementedError


##########


def file_detail(request, file_slug, file_sha256):
    print "%s: %s" % (file_slug, file_sha256)
    document = get_object_or_404(Document, slug=file_slug, sha256=file_sha256)
    print document
    raise NotImplementedError("TODO")


##########


def file_download(request, file_slug, file_sha256):
    document = get_object_or_404(Document, slug=file_slug, sha256=file_sha256)
    print document
    raise NotImplementedError("TODO")


##########


def file_signature(request, file_slug, file_sha256):
    document = get_object_or_404(Document, slug=file_slug, sha256=file_sha256)
    print document
    raise NotImplementedError("TODO")

def admin_login(request):
  logout(request)
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
       username = request.POST['Username']
       password = request.POST['Password']
       user = authenticate(username=username, password=password)
       if user is not None:
         if user.is_active:
           login(request, user)
           return HttpResponseRedirect('/admin/authapp')
  else:
    form = LoginForm() 
  
  return render(request, 'authentication/admin_login.html', {
                 'form': form
                })

@login_required
def admin_document(request):
  documents = Document.objects.all() 
  return render(request, 'authentication/document.html', {
                  'documents': documents
               })

@login_required
def admin_authapp(request):
  return render(request, 'authentication/admin_authapp.html')
