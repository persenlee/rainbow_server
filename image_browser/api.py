from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from image_browser.models import Image, Tags, Report, ImageReport, ImageTags
from image_browser.serializers import ImageSerializer
from user.service import UserService
import json


@api_view(['GET'])
def feeds(request):
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        per_page = int(request.GET.get('per_page', 10))
        sql = 'select ' \
              'image.id,' \
              'image.title,' \
              'image.src,' \
              'image.thumb_src,' \
              'image.tags,' \
              'ifnull(image_likes.count,0) as like_count ' \
              'from image ' \
              'left join image_likes on image.id=image_likes.image_id ' \
              'order by image.create_time'

        user_id = request.session.get('user_id', None)
        if user_id:
            sql = 'select ' \
                  'image.id,' \
                  'image.title,' \
                  'image.src,' \
                  'image.thumb_src,' \
                  'image.tags,' \
                  'ifnull(image_likes.count,0) as like_count,' \
                  '(case when t_likes.image_id is not null then true else false end) as favorite ' \
                  'from image ' \
                  'left join image_likes on image.id=image_likes.image_id ' \
                  'left outer join ' \
                  '(select image_id  from collect_images where collect_images.user_id=%d) t_likes ' \
                  'on image.id=t_likes.image_id ' \
                  'order by image.create_time' % (user_id)

        image_list = Image.objects.raw(sql)
        paginator = Paginator(image_list, per_page)
        try:
            image_page = paginator.page(page)
        except PageNotAnInteger:
            image_page = paginator.page(1)
        except EmptyPage:
            image_page = None

        serializer = ImageSerializer(image_page, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def like(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', None)
        user = UserService.request_user_info(user_id)
        if user:
            image_id = request.POST.get('id', None)
            star = request.POST.get('like', None)
            success = UserService.collect_image(user_id, image_id, star)
            if success:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def tags(request):
    if request.method == 'POST':
        image_id = int(request.POST.get('id'))
        tag_ids = request.POST.get('tag_ids', None)
        image = Image.objects.filter(id=image_id).first()
        if tag_ids and tag_ids != '' and image:
            record = ImageTags()
            record.image = image_id
            record.tags = tag_ids
            record.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def report(request):
    if request.method == 'POST':
        image_id = request.POST.get('id', None)
        report_id = request.POST.get('report_id', None)
        if image_id and image_id != '' and report_id and report_id != '':
            report_reason = request.POST.get('report_reason')
            report_obj = Report.objects.filter(id=report_id).first()
            image = Image.objects.filter(id=image_id).first()
            if report_obj and image:
                image_report = ImageReport()
                image_report.image = image_id
                image_report.report = report_id
                image_report.detail = report_reason
                image.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)
