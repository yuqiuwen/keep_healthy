from rest_framework import serializers
from rest_framework.fields import DateTimeField

from diabetes.models import Diabetes


class DiabetesModelSerializer(serializers.ModelSerializer):

    create_time = DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Diabetes
        fields = "__all__"
