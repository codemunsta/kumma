from .models import Faculty, Department, Student
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from .file_check import school_fees_check
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView


def register_view(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }

    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        return redirect('dashboard', pk=student.id)

    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['mat_number'])
            return redirect('login.html')
        except ObjectDoesNotExist:
            username = request.POST['mat_number']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            department = Department.objects.get(id=request.POST['department'])
            school_fees = request.FILES['school_fees']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                filestorage = FileSystemStorage()
                school_fees_pdf = filestorage.save(school_fees.name, school_fees)
                check_1 = school_fees_check(filestorage.path(school_fees_pdf), mat_no=username, session='2020/2021')
                if check_1 == 0:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.first_name = firstname
                    user.last_name = lastname
                    user.save()
                    student = Student.objects.create(
                        stud=user,
                        mat_no=username,
                        firstname=firstname,
                        lastname=lastname,
                        school_fees=school_fees_pdf,
                        uniben_email=email,
                        department=department,
                    )
                    student.save()
                    user = authenticate(request, username=username, password=password)
                    login(request, user)
                    student = Student.objects.get(stud=request.user)
                    return redirect('dashboard', pk=student.id)
                else:
                    return render(request, 'register.html', context)
            else:
                return render(request, 'register.html', context)
    else:
        return render(request, 'register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        return redirect('dashboard', pk=student.id)
    if request.method == 'POST':
        username = request.POST['mat_number']
        password = request.POST["password"]
        check_user = User.objects.filter(username=username).exists()
        if check_user is False:
            return redirect('login')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            student = Student.objects.get(stud=user)
            return redirect('dashboard', pk=student.id)
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')


def index(request):
    context = {}
    return render(request, 'index.html', context)


class Dashboard(DetailView):

    model = Student
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        student = Student.objects.get(stud=self.request.user)
        department = student.department
        faculty = department.faculty
        context['department'] = department
        context['faculty'] = faculty
        return context


def user_logout(request):
    logout(request)
    return redirect('index')
