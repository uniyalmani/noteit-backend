from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db import models


class UserManger(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        create and save user of given email, name, password
        """ 
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(email=self.normalize_email(email),
                          name=name,
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user



class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    username = models.CharField(max_length=40, unique=False, default='')
    
    objects = UserManger()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name
    
 