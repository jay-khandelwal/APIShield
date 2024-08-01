import uuid
from django.db import models

class Document(models.Model):
    owner = models.UUIDField(editable=False, unique=False)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
