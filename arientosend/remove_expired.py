from django.utils import timezone

from send.models import FileAccess
from send.models import File as ArientoFile

accesses = FileAccess.objects.all()
for access in accesses:
    if (access.file_expiration_date <= timezone.now() or access.download_count >= access.download_limit):
        arientoFile = access.file
        arientoFile.delete()
