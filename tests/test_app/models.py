from django import VERSION
from admin_customizer.fields import OrderPreservingManyToManyField
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    authors = OrderPreservingManyToManyField(Author)

class BookNote(models.Model):
    book = models.ForeignKey("Book", null=True)
    notes = models.TextField()
