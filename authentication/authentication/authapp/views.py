from django.shortcuts import render
#...
#from authentication.authapp.models import Document
#...

def index(request):
  return render(request, template_name='authentication/index.html')
