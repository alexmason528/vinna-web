from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
  account_id = serializers.IntegerField()
  business_id = serializers.IntegerField()
  review = serializers.FloatField(required = False)

  class Meta:
    model = Review
    fields = ('account_id', 'business_id', 'rating', 'review')

  def update(self, instance, validated_data):
    if 'account_id' in validated_data:
      validated_data.pop('account_id')
    if  'business_id' in validated_data:
      validated_data.pop('business_id')

    for item in validated_data:
      if Review._meta.get_field(item):
        setattr(instance, item, validated_data[item])
   
    instance.save()

    return instance
