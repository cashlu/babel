from account.models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        # fields = ["qsid", "name", "gender"]
        depth = 5
