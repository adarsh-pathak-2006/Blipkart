from django.db import models

class product(models.Model):
    name=models.CharField(max_length=150)
    description=models.TextField()
    price=models.IntegerField()
