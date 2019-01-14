from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse;
from user.models import MailCodeModel
from user.models import UserModel
from user.models import InvitationCodeModel
from django.conf import settings
from user.forms import *
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
import random


# Create your views here.
def login_page(request):
    context = {
    }
    request.session.set_test_cookie()
    return render(request, 'index.html', context)


def register_page(request):
    context = {
    }
    request.session.set_test_cookie()
    return render(request, 'register.html', context)


#注册
def sign_up(request):

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        clean_data = form.cleaned_data
        email = clean_data.get('email', None)
        password = clean_data.get('password', None)
        validate_code = clean_data.get('validate_code', None)
        invite_code = clean_data.get('invite_code', None)

        user = UserModel.objects.filter(email=email)
        if user:
            form.add_error(None, '邮箱已注册')
        else:
            user = UserModel()
            user.email = email
            encode_password = make_password(
                password
            )
            user.password = encode_password
            records = MailCodeModel.objects.filter(code=validate_code)
            if records:
                user.active = True

            invitation = InvitationCodeModel.objects.filter(code=invite_code, active=False)
            if invitation:
                invitation.active = True
                user.invite = True
                invitation.save()
            user.save()
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                request.session['user_id'] = user.id;
            return HttpResponseRedirect(reverse('image_browser:home'))

    return render(request, 'register.html', {'form': form})


def email_registered(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        user = UserModel.objects.filter(email=email)
        if user:
            return True
        else:
            return False


def get_mail_code(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        model = MailCodeModel.objects.filter(email=email)
        if not model:
            code = random_str(6)
            subject = '欢迎注册'
            message = '您的验证码%s' % code
            result = send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            if result:
                model = MailCodeModel()
                model.email = email
                model.code = code
                model.save()

                return Response({}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_403_FORBIDDEN)


#登录
def sign_in(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            clean_data = form.cleaned_data
            email = clean_data.get('email', None)
            password = clean_data.get('password', None)
            # encode_password = make_password(password)
            user = UserModel.objects.filter(email=email).first()

            if user:
                check_pass = check_password(password, user.password)
                if check_pass:
                    request.session['user_id'] = user.id
                    return HttpResponseRedirect(reverse('image_browser:home'))
            form.add_error(None, '用户名或密码不存在')
        else:
            return HttpResponse("Please enable cookies and try again.")
    return render(request, 'index.html', {'form': form})


def user_center(request):
    pass


def random_str(length=8):
    rstr = ''
    chars = '0123456789'
    chars_len = len(chars) - 1
    for i in range(length-1):
        rstr += chars[random.randint(0, chars_len-1)]
    return rstr
