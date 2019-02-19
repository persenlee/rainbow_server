from rest_framework import serializers
from image_browser.models import Image, Tags, Report


class ImageSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(default=0)
    favorite = serializers.BooleanField(default=False)

    class Meta:
        model = Image
        fields = ('id', 'title', 'src', 'thumb_src', 'tags', 'create_time', 'like_count', 'favorite')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'reason')
