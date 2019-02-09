from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserLoginActivity(models.Model):
	SUCCESS = 'S'
	FAILED = 'F'
	
	LOGIN_STATUS = (
		(SUCCESS, 'Success'),
		(FAILED, 'Failed')
	)
	
	login_IP = models.GenericIPAddressField(blank=True, null=True)
	login_date = models.DateTimeField(auto_now=True)
	login_username = models.CharField(max_length=40, blank=True, null=True)
	status = models.CharField(max_length=1, default=FAILED, choices=LOGIN_STATUS, null=True, blank=True)
	user_agent_info = models.CharField(max_length=255)
	
	class Meta:
		verbose_name = 'user login activity'
		verbose_name_plural = 'user login activities'


class CustomUserManager(BaseUserManager):
	def create_user(self, email, phone_number, password):
		email = self.normalize_email(email)
		user = self.model(email=email, phone_number=phone_number)
		user.set_password(password)
		user.is_staff = False
		user.is_superuser = False
		user.save(using=self._db)
		
		return user
	
	def create_superuser(self, email, phone_number, password):
		email = self.normalize_email(email)
		user = self.model(email=email, phone_number=phone_number)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		
		return user
	
	def get_by_natural_key(self, email_):
		return self.get(email=email_)


class User(AbstractUser):
	username = None
	email = models.EmailField(unique=True)
	phone_number = models.CharField(max_length=13)
	REQUIRED_FIELDS = ['phone_number']
	USERNAME_FIELD = 'email'
	
	objects = CustomUserManager()
	
	def get_short_name(self):
		return self.email
	
	def natural_key(self):
		return self.email
	
	def __str__(self):
		return self.email
