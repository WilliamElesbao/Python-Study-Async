from django.db import models
from django.contrib.auth.models import User

class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='books')
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title
    
class ViewBook(models.Model):
    ip = models.GenericIPAddressField()
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.ip
