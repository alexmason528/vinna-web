from rest_framework import serializers

class StripeManagedAccountSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=3, required=False)
    email = serializers.EmailField(required=True)
