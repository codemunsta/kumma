from django.shortcuts import render, redirect
from .models import Positions, Candidate
from users.models import Student, Department, Faculty


def vote_page(request):
    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        department = student.department
        faculty = department.faculty
        positions = Positions.objects.filter(faculty=faculty)
        if request.method == 'POST':
            data = request.POST
            votes = []
            for position in positions:
                var = data[f'{position.title}']
                if var == 'abstain':
                    pass
                else:
                    candidate = Candidate.objects.get(id=var)
                    item = {
                        'position': position.title,
                        'candidate': candidate
                    }
                    votes.append(item)
            context = {
                'votes': votes
            }
            return render(request, 'confirmation.html', context)
        else:
            polls = []
            for position in positions:
                candidates = Candidate.objects.filter(position=position)
                item = {
                    'position': position,
                    'candidates': candidates
                }
                polls.append(item)
            context = {
                'polls': polls
            }
            return render(request, 'voting.html', context)
    else:
        return redirect('login')


def confirmation(request):
    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        department = student.department
        faculty = department.faculty
        positions = Positions.objects.filter(faculty=faculty)
        if request.method == 'POST':
            data = request.POST
            for position in positions:
                try:
                    var = data[f'{position.title}']
                    candidate = Candidate.objects.get(id=var)
                    candidate.votes = candidate.votes + 1
                    candidate.save()
                except:
                    pass
            return render(request, 'confirmed.html')
    else:
        return redirect('login')

# Create your views here.
