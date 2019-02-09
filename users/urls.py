from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token

from .views import UserViewSet, AuthenticateUserView, UserRegistrationViewSet, UserChangePasswordViewSet

router = routers.DefaultRouter()

router.register('change-password', UserChangePasswordViewSet)
router.register('register', UserRegistrationViewSet)
router.register('users', UserViewSet)

urlpatterns = [
	path('login/', AuthenticateUserView.as_view()),
	path('refresh-token/', refresh_jwt_token),
]
urlpatterns += router.urls
