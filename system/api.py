from image_browser.models import Tags, Report
from image_browser.serializers import TagsSerializer, ReportsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


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
