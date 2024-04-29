from django.db import models
from django.contrib.auth import get_user_model

class Session(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
