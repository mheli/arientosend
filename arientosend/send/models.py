from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# User model for valid ariento users
class User(models.Model):
    email = models.CharField(max_length=30, unique=True)
    safenet_user = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.email

# File storage model
# File uploads help:
# https://docs.djangoproject.com/en/1.9/topics/http/file-uploads/
class File(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    file = models.FileField()

    def __str__(self):
        return self.key

# File Access Model, defines access method and who has permission to view file
class FileAccess(models.Model):
    ACCESS_TYPE = (
        ('P', 'Password'),
        ('U', 'User'),
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=1, choices=ACCESS_TYPE)
    ariento_user = models.ForeignKey(User)
    password = models.CharField(max_length=30)
    file_from_email = models.CharField(max_length=30)
    file_sent_date = models.DateTimeField(editable=False)
    file_expiration_date = models.DateTimeField()

    # call on model save
    def save(self, *args, **kwargs):
        # update timestamps
        self.file_sent_date = timezone.now()
        self.file_expiration_date = timezone.now()+timezone.timedelta(days=3)
        super(FileAccess, self).save(*args, **kwargs)

    def __str__(self):
        return self.file_from_email