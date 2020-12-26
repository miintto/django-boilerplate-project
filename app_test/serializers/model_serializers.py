from rest_framework import serializers
from app_test import models


class DumpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DumpModel
        fields = "__all__"
