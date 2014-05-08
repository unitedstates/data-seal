from django.contrib import admin
from models import Document


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

# Register your models here.
admin.site.register(Document, DocumentAdmin)
