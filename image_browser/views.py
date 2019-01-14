from django.shortcuts import render

# Create your views here.
from image_browser.models import Image, ImageLikeCount, ImageTags, Tags
from django.shortcuts import render
from image_browser.serializers import ImageSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from user.service import UserService
from django.urls import reverse
import json


def home(request):
    image_list = Image.objects.order_by('id')
    pageinator = Paginator(image_list, 10)
    page = request.GET.get('page')
    user_id = request.session.get('user_id', None)
    user = UserService.request_user_info(user_id) or None
    try:
        image_page = pageinator.page(page)
    except PageNotAnInteger:
        image_page = pageinator.page(1)
        page = "1"
    except EmptyPage:
        image_page = pageinator.page((pageinator.num_pages))

    scope = pageinator_range(
        pageinator.validate_number(page),
        pageinator.num_pages
    )

    like_dic = {}
    i_like_dic = {}
    for image in image_page:
        like_count_model = ImageLikeCount.objects.filter(image_id=image.id).first()
        like_count = like_count_model.count if like_count_model else 0
        like_dic[image.id] = like_count
        i_like = UserService.request_has_collect_image(user_id, image.id)
        i_like_dic[image.id] = i_like

    tag_list = Tags.objects.order_by('id')
    context = {
        'image_list': image_page,
        'user': user,
        'page_range': range(scope[0], scope[1]),
        'image_likes': like_dic,
        'i_likes': i_like_dic,
        'tag_list': tag_list
    }
    return render(request, 'home.html', context)



def pageinator_range(current_page, number_page, start_page=1, slice=5):
    min_page = max(current_page - slice, start_page)
    max_page = min(current_page + slice, number_page)
    offset = max_page - min_page
    left = slice + slice - offset
    for i in range(0, left):
        if i % 2:
            if max_page + 1 < number_page:
                max_page = max_page + 1
            elif min_page - 1 > 1:
                min_page = min_page - 1
        else:
            if min_page - 1 > start_page:
                min_page = min_page - 1
            elif max_page + 1 < number_page:
                max_page = max_page + 1
    return (min_page, max_page)

@csrf_exempt
def image_list(request):
    if request.method == 'GET':
        images = Image.objects.all().order_by('id')
        pageinator = Paginator(images, 10)
        page = request.GET.get('page')
        try:
            image_page = pageinator.page(page)
        except PageNotAnInteger:
            image_page = pageinator.page(1)
        except EmptyPage:
            image_page = None
        user_id = request.session.get('user_id', None)
        user = UserService.request_user_info(user_id) or None

        like_dic = {}
        i_like_dic = {}
        for image in image_page:
            like_count_model = ImageLikeCount.objects.filter(image_id=image.id).first()
            like_count = like_count_model.count if like_count_model else 0
            like_dic[image.id] = like_count
            i_like = UserService.request_has_collect_image(user_id, image.id)
            i_like_dic[image.id] = i_like

        tag_list = Tags.objects.order_by('id')
        context = {
            'image_list': image_page,
            'user': user,
            'image_likes': like_dic,
            'i_likes': i_like_dic,
            'tag_list': tag_list
        }
        return render(request, 'base.html', context)
        # serializer = ImageSerializer(image_page,many=True)
        # return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def star(request):
    if request.method == 'GET':
        image_id = request.GET.get('image_id')
        star = request.GET.get('star')
        user_id = request.session.get('user_id', None)
        if image_id:
            if user_id:
                result = UserService.collect_image(user_id, image_id, star)
                response = {'status': 1, 'message': "点赞成功"}
                return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                response = {'status': -101, 'message': "未登录"}
                return HttpResponse(json.dumps(response), content_type='application/json')
        response = {'status': 0, 'message': "无效的图片"}
        return HttpResponse(json.dumps(response), content_type='application/json')



def add_tag(request):
    if request.method == 'POST':
        image_id = int(request.POST.get('image_id'))
        tag_id = int(request.POST.get('tag_id'))
        image = Image.objects.filter(id=image_id).first()
        tag = Tags.objects.filter(id=tag_id).first()
        if image and tag:
            tags = json.loads(image.tags) if image.tags else []
            if tag_id not in tags:
                tags.append(tag_id)
                image.tags = json.dumps(tags)
                image.save()
                response = {'status': 1, 'message': "添加标签成功"}
                return HttpResponse(json.dumps(response), content_type='application/json')
    response = {'status': 0, 'message': "添加标签失败"}
    return HttpResponse(json.dumps(response), content_type='application/json')

def report_page(request):
    context = {}
    return render(request, 'report.html', context)


def report(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        reports = request.POST.get('reports')
