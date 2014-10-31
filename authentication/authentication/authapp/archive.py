import internetarchive
import os
from django.conf import settings

def export_to_ia(f):
    item = internetarchive.Item(settings.IA_ITEM)
    md = dict(creator=settings.IA_CREATOR)
    item.upload(f.doc_file, metadata=md, access_key=settings.IA_ACCESS_KEY, secret_key=settings.IA_SECRET_KEY)
    print unicode(f) + " uploaded to the Internet Archive"