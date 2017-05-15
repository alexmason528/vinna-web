from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, CustomJSONWebTokenSerializer, CustomVerificationBaseSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CustomObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = CustomJSONWebTokenSerializer

class CustomVerifyJSONWebToken(JSONWebTokenAPIView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """
    serializer_class = CustomVerificationBaseSerializer

custom_obtain_jwt_token = CustomObtainJSONWebToken.as_view()
custom_verify_jwt_token = CustomVerifyJSONWebToken.as_view()