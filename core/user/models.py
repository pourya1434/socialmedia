from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.abstract.models import AbstractManager, AbstractModel
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import uuid
# Create your models here.

class UserManager(BaseUserManager, AbstractManager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404

            
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a User with email phone number username and password"""
        if username is None:
            raise TypeError('User must have a username') 
        if email is None:
            raise TypeError('User must have a email')           
        if password is None:
            raise TypeError('User must have a password') 
        
        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, email, password, **kwargs):
        """Create and return user with admin permissions"""
        if password is None:
            raise TypeError('User must have a password') 
        if email is None:
            raise TypeError('User must have a email') 
        if username is None:
            raise TypeError('User must have a username') 
        
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class User(AbstractModel,AbstractBaseUser, PermissionsMixin):
    # public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False) #user AbstractModel no deffrence
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    bio=models.TextField(null=True)
    # avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # created = models.DateTimeField(auto_now=True)
    # updated = models.DateTimeField(auto_now_add=True)

    posts_liked = models.ManyToManyField("core_post.Post",related_name='liked_by' )

    def like(self, post):
        return self.posts_liked.add(post)
    
    def remove_like(self, post):
        return self.posts_liked.remove(post)
    
    def has_liked(self, post):
        return self.posts_liked.filter(pk=post.pk).exists()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    
    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
        