from django.contrib import admin
from models import Document


class DocumentAdmin(admin.ModelAdmin):
  pass
# Register your models here.
admin.site.register(Document, DocumentAdmin)
