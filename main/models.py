from django.db import models
from django.contrib.auth.models import User
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  # item name
    price = models.IntegerField()  # item price
    description = models.TextField()  # item description
    thumbnail = models.URLField(max_length=500)  # item image URL
    category = models.CharField(max_length=100)  # item category
    is_featured = models.BooleanField(default=False)  # featured status
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return self.name
