from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField()
    business_id = serializers.IntegerField()
    review = serializers.CharField(required = False)

    class Meta:
        model = Review
        fields = ('member_id', 'business_id', 'rating', 'review')

    def update(self, instance, validated_data):

        if 'member_id' in validated_data:
            validated_data.pop('member_id')
        if  'business_id' in validated_data:
            validated_data.pop('business_id')

        for item in validated_data:
            if Review._meta.get_field(item):
                setattr(instance, item, validated_data[item])
       
        instance.save()

        return instance
