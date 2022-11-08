import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

# User = get_user_model()
from auth_app.models import Users as User
from search_app.models import UserInput


class InputSaveSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    inputs = serializers.CharField(max_length=255)

    def create(self, validated_data):
        inputs = [x.strip() for x in validated_data.get('inputs').split(",")]
        user = validated_data.get('user')
        timenow = datetime.datetime.now()
        for i in inputs:
            UserInput.objects.create(user=user, input=i, date_created=timenow)
        return validated_data


class InputSearchSerializer(serializers.Serializer):
    input = serializers.IntegerField()
