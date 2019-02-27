from image_browser.models import Tags, Report
from image_browser.serializers import TagsSerializer, ReportsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from qiniu import Auth


@csrf_exempt
@api_view(['GET'])
def config(request):
    if request.method == 'GET':
        tags = Tags.objects.order_by('id')
        reports = Report.objects.order_by('id')
        tags_serializer = TagsSerializer(tags, many=True)
        report_serializer = ReportsSerializer(reports, many=True)
        result = {'tags': tags_serializer.data, 'reports': report_serializer.data}
        return Response(data=result, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def upload_token(request):
    if request.method == 'GET':
        # 需要填写你的 Access Key 和 Secret Key
        access_key = 'znatQfVkHSRN_f6wGMIb8VMYyzOCYu_lJcpC-M80'
        secret_key = '07Z9VBmgi2L4gapEImXSukbFO1tCKx9A7qeg8-sg'
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = 'rainbow'
        # 上传后保存的文件名
        key = None
        # 生成上传 Token，可以指定过期时间等
        # 上传策略示例
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        policy = {
            # 'callbackUrl':'https://requestb.in/1c7q2d31',
            # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
            # 'persistentOps':'imageView2/1/w/200/h/200'
        }
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name, key, 3600 * 6, policy)
        result = {'token': token}
        return Response(data=result, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
