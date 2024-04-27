from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class User(models.Model):
    #UserId = models.CharField(max_length=3)
    UserName = models.CharField(max_length=200)
    #EmpGender = models.CharField(max_length=10)
    UserEmail = models.EmailField()
    #EmpDesignation = models.CharField(max_length=150)
    #EmpPhoto = models.ImageField(upload_to='photos/', blank=True, null=True)
    class Meta:
        db_table="User"
