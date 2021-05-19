from rest_framework import viewsets,permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from app.vistor_mgt.models import NewVistor
from app.user.models import User,RoleManagement
from app.estate_mgt.models import Estate
from .serializers import *

# Create your views here.
class VisitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Visitors to be viewed or edited.
    """
    queryset = NewVistor.objects.all()
    serializer_class = VisitorInviteSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Visitors to be viewed or edited.
    """
    queryset = RoleManagement.objects.all()
    serializer_class = RoleManagementSerializer


class EstateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Visitors to be viewed or edited.
    """
    queryset = Estate.objects.all()
    serializer_class = EstateManagementSerializer

class AuthTokenClass(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'message':'success'},)


class LoginUserViewSet(viewsets.ViewSet):
    """This Class Verifies and Logs in tthe User"""
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the AuthToken Obatined to create and Validate the auth token"""
        token = AuthTokenClass().post(request)
        return token