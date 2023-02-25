from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, tg_id, password=None, **extra_fields):
        if tg_id is None:
            raise ValueError("tg_id не был передан")
        user = self.model(tg_id=tg_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, tg_id=0, **extra_fields):
        """
        Creates and saves a superuser with the given tg_id and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(tg_id, password, **extra_fields)
