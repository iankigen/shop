from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.permissions import IsAuthenticated, AllowAny

from .permissions import IsOwnerUpdate
from .serializers import User, UserSerializer, AuthenticateJWTSerializer, \
						  UserRegistrationSerializer, UserPasswordChangerSerializer


class UserViewSet(ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated, IsOwnerUpdate)
	http_method_names = ['get', 'put', 'patch']


class UserRegistrationViewSet(ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserRegistrationSerializer
	permission_classes = (AllowAny,)
	http_method_names = ['post']


class UserChangePasswordViewSet(ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserPasswordChangerSerializer
	permission_classes = (IsAuthenticated,)
	http_method_names = ['put']


class AuthenticateUserView(ObtainJSONWebToken):
	serializer_class = AuthenticateJWTSerializer
