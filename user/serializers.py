from rest_framework import  serializers
from user.models import UserModel

class UserModelSerializer(serializers.Serializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'avatar','age','gender','email')