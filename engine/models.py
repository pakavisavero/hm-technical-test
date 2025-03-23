from django.db import models

class Module(models.Model):
    name = models.CharField(max_length=255, unique=True)
    installed = models.BooleanField(default=False)
    version = models.CharField(max_length=50, default="1.0.0")

    def __str__(self):
        return self.name
