# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at =  models.DateTimeField(auto_now_add = True)
    updated_at =  models.DateTimeField(auto_now = True)
    
    def __str__(self):
       return self.first_name + " " + self.last_name

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at =  models.DateTimeField(auto_now_add = True)
    updated_at =  models.DateTimeField(auto_now = True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books')
    created_at =  models.DateTimeField(auto_now_add = True)
    updated_at =  models.DateTimeField(auto_now = True)

    def __str__(self):
       return self.title

class Review(models.Model):
    detail = models.TextField()
    rating = models.CharField(max_length=25)
    book = models.ForeignKey(Book, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews')
    created_at =  models.DateTimeField(auto_now_add = True)
    updated_at =  models.DateTimeField(auto_now = True)

