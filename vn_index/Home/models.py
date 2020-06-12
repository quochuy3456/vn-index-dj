from django.db import models

# Create your models here.
class Link(models.Model):
    code=models.CharField(max_length=5)
    link=models.CharField(max_length=200)

    def __str__(self):
        return self.code
