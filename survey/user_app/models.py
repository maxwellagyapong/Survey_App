from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
	def create_user(self, username, password=None):
		user = self.model(
			username=username
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password):
		user = self.create_user(
			username=username,
			password=password
		)
		user.is_admin = True
		user.is_superuser = True
		user.is_staff = True
		user.is_active = True

		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	# =====================================
	# General fields
	# =====================================
	username = models.CharField(max_length=20, unique=True)
		
	# =====================================
	# General default stuff
	# =====================================
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last joined', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	hide_email = models.BooleanField(default=True)

	objects = MyAccountManager()

	USERNAME_FIELD = 'username'

	class Meta:
		verbose_name_plural = "Users"

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True