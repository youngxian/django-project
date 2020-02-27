from django.db import models


# Create your models here.

# Create your models here.
class Connection(models.Model):
    connection_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.connection_id


class ChatMessage(models.Model):
    username = models.CharField(max_length=50, null=True)
    content = models.CharField(max_length=400, null=True)
    timestamp = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.content
