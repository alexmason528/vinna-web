from rest_framework import serializers
from .invitation_model import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    business_id = serializers.IntegerField()

    class Meta:
        model = Invitation
        fields = ('id', 'business_id', 'email', 'type')
