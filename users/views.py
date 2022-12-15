from django.shortcuts import render
from .models import Student
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
import base64
from django.core.files.base import ContentFile
from .file_check import school_fees_check
from django.core.files.storage import FileSystemStorage


class StudentRegister(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return Response({'message': 'user already exist, login to continue'}, status=status.HTTP_409_CONFLICT)
            raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            data = request.data
            try:
                User.objects.get(username=data['mat_number'])
                return Response({'message': 'email already exist'}, status=status.HTTP_409_CONFLICT)
            except ObjectDoesNotExist:
                username = data['mat_number']
                firstname = data['firstname']
                lastname = data['lastname']
                email = data['email']
                school_fees = data['school_fees']
                password = data['password']
                password2 = data['password2']
                if password == password2:
                    filestorage = FileSystemStorage()
                    school_fees_pdf = filestorage.save(school_fees.name, school_fees)
                    check_1 = school_fees_check(filestorage.path(school_fees_pdf), mat_no=username, session='2020/2021')
                    if check_1 == 0:
                        user = User.objects.create_user(username, email, password)
                        user.first_name = firstname
                        user.last_name = lastname
                        user.save()
                        user = User.objects.get(username=username)
                        student = Student.objects.create(
                            stud=user,
                            mat_no=username,
                            firstname=firstname,
                            lastname=lastname,
                            uniben_email=email,
                            school_fees=school_fees_pdf,
                        )
                        student.save()
                        return Response({'message': 'Registration Successful'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'message': 'School_fees provided not vaild'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'invalid password, or password mismatch'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    mat_number = request.data["mat_number"]
    password = request.data["password"]

    check_user = User.objects.filter(username=mat_number).exists()
    if check_user is False:
        msg = {"status": False, "message": f"User with the mat_number {mat_number} does not exists."}
        return Response(msg, status=status.HTTP_404_NOT_FOUND)

    userr = User.objects.get(username=mat_number)
    user = authenticate(username=userr.username, password=password)

    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=user)
            token.save()
        login(request, user)
        data = {
            'token': f'Token {token.key}',
            'username': user.username,
            'msg': {
                'status': True,
                'message': 'successfully logged in'
            }
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        msg = {"status": False, "message": "Invalid email/Password."}
        return Response(msg, status=status.HTTP_409_CONFLICT)


def logout_view():
    pass
# Create your views here.
