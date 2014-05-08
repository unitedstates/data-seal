from django import forms
from django.shortcuts import get_object_or_404, render
from authentication.authapp.models import Document


def index(request):
    return render(request, 'authentication/index.html')


##########


class UploadForm(forms.Form):
    user_file = forms.FileField(label="File you want to check")


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
