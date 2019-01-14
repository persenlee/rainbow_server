from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class UserModel(models.Model):
    class Meta:
        db_table = "user"
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=12)
    avatar = models.URLField()
    age = models.IntegerField(default=0)
    gender = models.IntegerField(default=0)
    mobile = models.CharField(max_length=11)
    create_time = models.DateTimeField(default=timezone.now())
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=False)
    invite = models.BooleanField(default=False)


class UserLoginModel(models.Model):
    class Meta:
        db_table = "user_login"
    user = models.ForeignKey(
        'UserModel',
        on_delete=models.CASCADE,
    )
    login_time = models.DateTimeField()
    user_agent = models.CharField(max_length=256)


class InvitationCodeModel(models.Model):
    class Meta:
        db_table = 'invitation_code'
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=6)
    active = models.BooleanField(default=False)



class CollectImagesModel(models.Model):
    class Meta:
        db_table = 'collect_images'
        unique_together = ("user", "image")
    user = models.ForeignKey(
        'UserModel',
        db_column='user_id',
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        'image_browser.Image',
        db_column='image_id',
        on_delete=models.CASCADE,
    )


class MailCodeModel(models.Model):
    class Meta:
        db_table = 'mail_code'
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    update_time = models.DateTimeField(default=timezone.now())


