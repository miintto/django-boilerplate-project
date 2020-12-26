from rest_framework import serializers


class ContentIdxSerializer(serializers.Serializer):
    contents_id = serializers.IntegerField(required=True)

class ContentsListSerializer(serializers.Serializer):
    category = serializers.CharField(required=True)
    order_by = serializers.CharField(required=True)
