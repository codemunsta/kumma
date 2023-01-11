from django.db import models
from users.models import Faculty, Department


class Positions(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=50)
    session = models.CharField(max_length=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Candidate(models.Model):
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    mat_no = models.CharField(max_length=15)
    about = models.TextField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to=f'images/candidate')
    votes = models.IntegerField()

    def __str__(self):
        return f'{self.firstname}, {self.lastname}'


class Result(models.Model):
    position = models.ForeignKey(Positions, on_delete=models.SET_NULL, null=True, blank=True)
    total_votes = models.IntegerField()
    winning_vote = models.IntegerField(null=True, blank=True)
    winner = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.position.name} | result'

# Create your models here.
