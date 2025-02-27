from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    picture = models.ImageField(upload_to='pictures_user', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Posts(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    picture = models.ImageField(upload_to='pictures_post', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Comments(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
