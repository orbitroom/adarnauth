from django.contrib.auth.models import BaseUserManager
from django import forms
from eveonline.managers import EVEManager
from datetime import datetime

class UserManager(BaseUserManager):
    def _create_user(self, main_character_id, email=None, is_staff=False, is_superuser=False, password=None, **extra_fields):
        if not main_character_id:
            raise ValueError('Users require a main character')
        if email:
            email = self.normalize_email(email)
        user = self.model(main_character_id=main_character_id, email=email, is_staff=is_staff, is_active=False, is_superuser=is_superuser, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        main_character = EVEManager.get_character_by_id(main_character_id)
        user.save()
        main_character.user = user
        main_character.save()
        return user

    def create_user(self, main_character_id, email=None, **extra_fields):
        return self._create_user(main_character_id, email, **extra_fields)

    def create_superuser(self, main_character_id, **extra_fields):
        user = self._create_user(main_character_id=main_character_id, is_staff=True, is_superuser=True, **extra_fields)
        user.is_active=True
        user.save()
        return user
