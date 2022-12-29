from django.db import models
from users.models import User


class Contact(models.Model):
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    secondname = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    post = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)
    creator_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.lastname} {self.firstname} {self.secondname}"
