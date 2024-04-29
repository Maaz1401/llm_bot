from django.db import models
from api.app_data import *

def get_file_path(self, filename):
    return f'files/{filename}'

class Document(models.Model):
    name = models.CharField(max_length=100)
    path = models.FileField(upload_to=get_file_path)

    def __str__(self):
        return f'{self.path.name}'
