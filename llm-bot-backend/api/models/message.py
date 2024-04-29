from django.db import models

class Message(models.Model):

    TYPE_TEXT = 1
    TYPE_DOCUMENT = 2
    TYPE_CHOICES = (
        (TYPE_TEXT, 'Text'),
        (TYPE_DOCUMENT, 'Document'),
    )
    message_type = models.IntegerField(default=TYPE_TEXT, choices=TYPE_CHOICES)
    session = models.ForeignKey('Session', on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    role = models.CharField(max_length=50)
    content = models.TextField()
    document = models.OneToOneField('Document', on_delete=models.SET_NULL, null=True, blank=True, related_name='message')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.text:
            return self.text
        return None

    class Meta:
        ordering = ['id']