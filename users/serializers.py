from rest_framework import serializers
from rest_framework import serializers
from users.models import User


class UserModelSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    password = serializers.CharField()
    is_remember = serializers.BooleanField()
    # verify_code = serializers.CharField(label='验证码', write_only=True)

    class Meta:
        model = User
        fields = "__all__"
