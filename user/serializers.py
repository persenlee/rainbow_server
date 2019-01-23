from rest_framework.serializers import ModelSerializer
from user.models import UserModel


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'avatar', 'age', 'gender', 'email', 'active', 'invite')
