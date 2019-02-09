import logging
from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver

from users.utils import get_client_ip
from .models import UserLoginActivity

error_log = logging.getLogger('error')


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
	try:
		user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
		user_login_activity_log = UserLoginActivity(
			login_IP=get_client_ip(request),
			login_username=user.username,
			user_agent_info=user_agent_info,
			status=UserLoginActivity.SUCCESS
		)
		user_login_activity_log.save()
	except Exception as e:
		error_log.error('log_user_logged_in request: {}, error: {}'.format(request, e))


@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
	try:
		user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
		user_login_activity_log = UserLoginActivity(
			login_IP=get_client_ip(request),
			login_username=credentials['username'],
			user_agent_info=user_agent_info,
			status=UserLoginActivity.FAILED
		)
		user_login_activity_log.save()
	except Exception as e:
		error_log.error('log_user_logged_in request: {}, error: {}'.format(request, e))
