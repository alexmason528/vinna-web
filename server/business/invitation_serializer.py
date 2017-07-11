from django.core.exceptions import ValidationError

from rest_framework import serializers

from .invitation_model import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    business_id = serializers.IntegerField()

    class Meta:
        model = Invitation
        fields = ('id', 'business_id', 'email', 'type')

    def create(self, validated_data):
        if Invitation.objects.filter(business_id = validated_data['business_id'], email = validated_data['email']).count() > 0:
            raise ValidationError('You already sent invitation to this user - ' + validated_data['email'])

        invitation = Invitation.objects.create(**validated_data)
        return invitation
