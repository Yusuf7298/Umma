from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile')
    bio = models.CharField(max_length=100, default='No bio...',blank=True)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        expiration_period = timezone.now() - timezone.timedelta(hours=24)
        return self.created_at < expiration_period

    def __str__(self):
        return f"Verification for {self.user.email}"


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='stories/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Story by {self.user.username} at {self.created_at}"

class Relationship(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    
    is_friends = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower} follows {self.followed}"


class CustomUser(models.Model):
    @property
    def friends(self):
        return User.objects.filter(
            models.Q(followers__follower=self, followers__is_friends=True) |
            models.Q(following__followed=self, following__is_friends=True)
        ).distinct()
    
    def get_followers(self):
        return self.followers.all().values_list('follower', flat=True)
    
    def get_following(self):
        return self.following.all().values_list('followed', flat=True)
    
    

