from django.db import models


# Create your models here.
class WOE(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title


class CH(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()

    def __str__(self):
        return str(self.id)
