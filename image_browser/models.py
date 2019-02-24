from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Image(models.Model):
    class Meta:
        db_table = "image"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    src = models.CharField(max_length=512)
    create_time = models.DateTimeField()
    thumb_src = models.CharField(max_length=512)
    tags = models.CharField(max_length=128, default='')


class ImageTags(models.Model):
    class Meta:
        db_table = 'image_tags'

    image = models.IntegerField()
    tags = models.CharField(max_length=64)
    active = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=timezone.now())


class Tags(models.Model):
    class Meta:
        db_table = 'tags'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)


class Report(models.Model):
    class Meta:
        db_table = 'report'

    id = models.AutoField(primary_key=True)
    reason = models.CharField(max_length=32)


class ImageReport(models.Model):
    class Meta:
        db_table = 'image_report'

    image = models.IntegerField()
    report = models.IntegerField()
    detail = models.CharField(max_length=100)


class ImageLikeCount(models.Model):
    class Meta:
        db_table = 'image_likes'
        managed = False

    image_id = models.IntegerField(primary_key=True)
    count = models.IntegerField(default=0)
