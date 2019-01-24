from rest_framework import serializers
from image_browser.models import Image, Tags


class ImageSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(default=0)
    like = serializers.BooleanField(default=False)

    class Meta:
        model = Image
        fields = ('id', 'title', 'src', 'thumb_src', 'tags', 'create_time', 'like_count', 'like')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')
