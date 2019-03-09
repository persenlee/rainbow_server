from user.models import UserModel, MailCodeModel, InvitationCodeModel, CollectImagesModel
from django.contrib.auth.hashers import check_password, make_password
from user.forms import LoginForm, RegisterForm, ProfileForm, MailForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
import random
from user.serializers import UserModelSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from image_browser.models import Image
from image_browser.serializers import ImageSerializer


@api_view(['POST'])
def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        clean_data = form.cleaned_data
        email = clean_data.get('email', None)
        password = clean_data.get('password', None)
        user = UserModel.objects.filter(email=email).first()

        if user:
            check_pass = check_password(password, user.password)
            if check_pass:
                serializer = UserModelSerializer(user)
                # if request.session.test_cookie_worked():
                #     request.session.delete_test_cookie()
                request.session['user_id'] = user.id
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        form.need_confirm = False
        if form.is_valid():
            clean_data = form.cleaned_data
            email = clean_data.get('email', None)
            password = clean_data.get('password', None)
            validate_code = clean_data.get('validate_code', None)
            invite_code = clean_data.get('invite_code', None)

            user = UserModel.objects.filter(email=email)
            if user:
                return Response(status=status.HTTP_409_CONFLICT)
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
                return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def mail_code(request):
    if request.method == 'POST':
        form = MailForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email', None)
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
                    return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def email_used(request):
    if request.method == 'GET':
        form = MailForm(request.GET or None)
        if form.is_valid():
            email = form.cleaned_data.get('email', None)
            users = UserModel.objects.filter(email=email)
            result = {"used": False}
            if len(users) > 0:
                result["used"] = True
            return Response(data=result, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_id = request.session.get('user_id', None)
            user = UserModel.objects.filter(id=user_id).first()
            if user:
                modified_dic = {k: v for k, v in form.cleaned_data.items() if v is not None and v != ''}
                for key, value in modified_dic.items():
                    if key == 'id' or ((key == 'active' or key == 'invite') and value == False):
                        continue
                    else:
                        setattr(user, key, value)

                user.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        user_id = request.session.get('user_id', None)
        if user_id:
            user = UserModel.objects.filter(id=user_id).first()
            if user:
                serializer = UserModelSerializer(user)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def likes(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        page = request.GET.get('page')
        per_page = request.GET.get('per_page', 10)
        like_relation = CollectImagesModel.objects.filter(user=user_id).order_by('create_time').values_list('image',
                                                                                                            flat=True)
        paginator = Paginator(like_relation, per_page)
        try:
            like_page = paginator.page(page)
        except PageNotAnInteger:
            like_page = paginator.page(1)
        except EmptyPage:
            like_page = None

        if like_page:
            image_ids = like_page.object_list
            image_id_str = [str(x) for x in image_ids]
            ids_str = "(%s)" % (','.join(image_id_str))
            sql = 'select ' \
                  'image.id,' \
                  'image.title,' \
                  'image.src,' \
                  'image.thumb_src,' \
                  'image.tags,' \
                  'ifnull(image_likes.count,0) as like_count,' \
                  'true as favorite ' \
                  'from image ' \
                  'left join image_likes ON image.id=image_likes.image_id ' \
                  'where id in %s' % ids_str
            image_obj = Image.objects.raw(sql)
            serializer = ImageSerializer(image_obj, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def random_str(length=8):
    result = ''
    chars = '0123456789'
    chars_len = len(chars) - 1
    for i in range(length - 1):
        result += chars[random.randint(0, chars_len - 1)]
    return result
