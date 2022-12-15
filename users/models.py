from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Student(models.Model):
    stud = models.OneToOneField(User, on_delete=models.CASCADE)
    mat_no = models.CharField(max_length=15)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    school_fees = models.FileField(upload_to=f'student/school_fees')
    uniben_email = models.EmailField()

    def __str__(self):
        return f'{self.firstname}, {self.lastname}'

    def get_absolute_url(self):
        return reverse('dashboard', kwargs={'mat_no': self.mat_no})
# Create your models here.
