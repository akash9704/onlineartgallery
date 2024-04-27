from django.db import models
import os
from django.contrib.auth import get_user_model
from datetime import datetime
# Create your models here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

User = get_user_model()


# Artist
class Artist(models.Model):

    artist_name = models.CharField(max_length=300 , null = False, blank = False)
    speciality = models.CharField(max_length=300,null = False, blank = False)

# Art


class Art(models.Model):
    art_name = models.CharField(max_length=50, null=False, blank=False)
    art_artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=os.path.join(BASE_DIR, "media"))
    price = models.FloatField(null=False, blank=False)
    instock = models.BooleanField(null = False,blank=False, default=True)
    description = models.TextField(null=False, blank=False)

# TAGs
class Tag(models.Model):

    tag = models.CharField(max_length=300, null=False)
    artid = models.ForeignKey(Art, on_delete=models.CASCADE)

# Cart Table

class MyCart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_id = models.ForeignKey(Art, on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=datetime.now())


# Order Table


class MyOrder(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    art_id = models.ForeignKey(Art, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())



class Address(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    town_city = models.CharField(max_length=255)
    postcode_zip = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email_address = models.EmailField()
    apartment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.country}"

