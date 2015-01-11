import json
import os
from zipfile import ZipFile, is_zipfile
from tempfile import mkdtemp
from shutil import rmtree
from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import TextInput, Textarea, CheckboxInput
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404

from authentication.authapp.models import Document

def index(request):
    return render(request, 'authentication/index.html')

##########

def documents(request):
    return render(request, 'authentication/documents.html', {"documents":Document.objects.all().order_by('doc_file')})

##########


class UploadForm(forms.Form):
    user_file = forms.FileField(label="File you want to check")

class LoginForm(forms.Form):
    Username = forms.CharField(max_length=50)
    Password = forms.CharField(max_length=50)

class DocumentForm(forms.ModelForm):
  class Meta:
    model = Document
    fields = ['doc_file', 'name', 'description', 'license']
    widgets = {
               'name': TextInput(attrs={'class': 'form-control'}),
               'description': Textarea(attrs={'class': 'form-control'}),
               'license': Textarea(attrs={'class': 'form-control'}),
              }

class UserForm(forms.ModelForm):
  is_staff = forms.BooleanField(label="Admin", widget = CheckboxInput(), required=False)
  class Meta:
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
    widgets = {
               'username': TextInput(attrs={'class': 'form-control'}),
               'password': TextInput(attrs={'class': 'form-control'}),
               'first_name': TextInput(attrs={'class': 'form-control'}),
               'last_name': TextInput(attrs={'class': 'form-control'}),
               'email': TextInput(attrs={'class': 'form-control'}),
               }

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
                return HttpResponse(json.dumps({
                                      'document': {"name":unicode(document), "sha512":document.sha512, "uploaded":str(document.uploaded)},
                                      'validation': {"is_valid":validation.valid, "fingerprint":validation.fingerprint}}), 
                                    content_type = "application/json")
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

def file_detail(request, doc_id, file_sha256):
    print "%s: %s" % (doc_id, file_sha256)
    document = get_object_or_404(Document, doc_id=doc_id, sha256=file_sha256)
    print document
    raise NotImplementedError("TODO")

##########


def file_download(request, file_slug, file_sha256):
    document = get_object_or_404(Document, slug=file_slug, sha256=file_sha256)
    print document
    raise NotImplementedError("TODO")


##########

def file_signature(request, file_sha256, file_name):
    document = get_object_or_404(Document, sha256=file_sha256)
    if os.path.basename(document.doc_file.name) == file_name:
      return HttpResponse(document.gpgsig, content_type='text/plain')
    else:
      raise Http404

def admin_login(request):
  if(request.user.is_authenticated()):
    return HttpResponseRedirect('/admin/authapp/')
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
def admin_logout(request):
  logout(request)
  return HttpResponseRedirect('/admin/login')

@staff_member_required
def admin_user(request):
  users = User.objects.all()
  return render(request, 'authentication/users.html', {
                  'users': users
                })

@staff_member_required
def admin_user_add(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      new_user.set_password(form.cleaned_data['password'])
      new_user.save()
      return HttpResponseRedirect('/admin/auth/user/')
  form = UserForm()
  return render(request, 'authentication/admin_user_add.html', {
                 'form': form,
                 'action': 'Add'
               })

@staff_member_required
def admin_user_edit(request, user_id):
  old_user = User.objects.get(id=user_id)
  if request.method == 'POST':
    form = UserForm(request.POST, instance=old_user)
    if form.is_valid():
      updated_user = form.save()
      if len(form.cleaned_data['password']) < 30:
        updated_user.set_password(form.cleaned_data['password'])
        updated_user.save()
      return HttpResponseRedirect('/admin/auth/user/')
  form = UserForm(instance=old_user)
  return render(request, 'authentication/admin_user_add.html', {
                 'form': form,
                 'action': 'Edit'
               })
      
@login_required
def admin_document(request):

  if request.method == 'POST':
    doc_id = request.POST['doc_id']
    d = Document.objects.get(id=doc_id)
    d.delete()
    return HttpResponse()
  else:
    documents = Document.objects.all() 
    return render(request, 'authentication/document.html', {
                    'documents': documents
                 })

@login_required
def admin_authapp(request):
  return render(request, 'authentication/admin_authapp.html')

def handleZipFile(input_file, subpath):
  # keep track of # of inner files we have (so we can report this
  # back to the user later)
  num_files = 0

  # we'll unzip the zip file to a temporary directory and *then*
  # pass the files into Django.
  tempdir = mkdtemp()

  #Extract all files from zip
  z = ZipFile(input_file)
  z.extractall(tempdir)

  for name in z.namelist():
    # the full path to file, inside temp directory.
    file_loc = os.path.join(tempdir, name)

    # skip if we don't want it in our db
    if name.startswith('__MACOSX/') or os.path.isdir(file_loc):
      continue

    # now create a Document and send this file into Django's
    # magic file handling.
    # "/document/2014/06/<filename>"
    save_name = os.path.join(subpath, name)

    if Document.find_user_file(open(file_loc, 'r')).first() == None:

      new_doc = Document()
      with open(file_loc, 'rb') as f:
        new_doc.doc_file.save(save_name, File(f))
      new_doc.save()
      num_files += 1

      #If this file was another zip file, unzip it too.
      if is_zipfile(file_loc):
        new_subpath = os.path.dirname(new_doc.doc_file.url)
        num_files += handleZipFile(file_loc, new_subpath)

  # Clear temp
  rmtree(tempdir)

  return num_files


@login_required
def add(request):
  if request.method == 'POST':
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
      # Check to see if the file is already in the system
      if Document.find_user_file(request.FILES['doc_file']).first() == None:
        new_doc = form.save()
        #Handle zip files
        if is_zipfile(request.FILES['doc_file']):
          url_subpath = os.path.dirname(new_doc.doc_file.url)
          num_inner_files = handleZipFile(request.FILES['doc_file'], url_subpath)
          if num_inner_files > 0:
            messages.add_message(request, messages.INFO, "Note: %d files inside the zip file were also saved as separate documents." % num_inner_files)
        return HttpResponseRedirect('/admin/authapp/document/'+str(new_doc.id))
      else:
        messages.add_message(request, messages.INFO, "Note: This document is already in the system")
  form = DocumentForm()
  return render(request, 'authentication/add.html', {
                 'form': form
               })

@login_required
def edit(request, file_id):
  old_doc = Document.objects.get(id=file_id)
  if request.method == 'POST':
    form = DocumentForm(request.POST, request.FILES, instance=old_doc)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/admin/authapp/document/'+str(old_doc.id))
  form = DocumentForm(instance=old_doc)
  return render(request, 'authentication/edit.html', {
                 'form': form,
                 'doc': old_doc
               })
      
