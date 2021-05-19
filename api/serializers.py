from app.vistor_mgt.models import NewVistor
from app.user.models import User, RoleManagement
from app.estate_mgt.models import Estate
from rest_framework import serializers


class VisitorInviteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewVistor
        fields = ['vistor_first_name', 'vistor_last_name', 'vistor_mobile_number', 'whom_to_see','estate']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'role', 'estate', 'password']


class RoleManagementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoleManagement
        fields = ['url','role_title']


class EstateManagementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Estate
        fields = ['url', 'estate_name', 'estate_address']