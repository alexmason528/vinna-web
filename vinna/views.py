from rest_framework_jwt.views import JSONWebTokenAPIView
from .serializers import CustomJSONWebTokenSerializer, CustomVerifyJSONWebTokenSerializer

class CustomObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = CustomJSONWebTokenSerializer

class CustomVerifyJSONWebToken(JSONWebTokenAPIView):
    """
    API View that checks the veracity of a token, returning the token if it
    is valid.
    """
    serializer_class = CustomVerifyJSONWebTokenSerializer

custom_obtain_jwt_token = CustomObtainJSONWebToken.as_view()
custom_verify_jwt_token = CustomVerifyJSONWebToken.as_view()
