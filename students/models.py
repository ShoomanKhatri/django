from django.db import models
from django.urls import reverse 

class Student(models.Model):
    name = models.CharField(max_length=100)
    email  = models.EmailField()
    age = models.IntegerField()

def __str__(self):
    return self.name

def get_absolute_url(self):
    return reverse('student_detail', kwarg={'pk': self.pk})


# Create your models here.
