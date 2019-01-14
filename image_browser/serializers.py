from rest_framework import serializers
from image_browser.models import Image, Tags


class ImageSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=128)
    # src = serializers.CharField(max_length=512)
    #
    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return Image.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.src = validated_data.get('code', instance.src)
    #     instance.save()
    #     return instance
    class Meta:
        model = Image
        fields = ('id', 'title', 'src')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')