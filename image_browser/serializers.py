from rest_framework import serializers
from image_browser.models import Image, Tags


class ImageSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField()
    class Meta:
        model = Image
        fields = ('id', 'title', 'src', 'thumb_src', 'tags', 'create_time', 'like_count')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')
