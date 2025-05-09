from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')  
    title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text='optional') 
    content = models.TextField(blank=True)
    image_file = models.ImageField(upload_to='blog_images', null=True, blank=True)
    videos_file = models.FileField(upload_to='blog_videos', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Blog post without title"

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.title:
                self.slug = slugify(self.title)
            else:
                self.slug = slugify(self.date_created) 
            original_slug = self.slug
            num = 1
            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{num}"
                num += 1
        

        super().save(*args, **kwargs)
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE , related_name='comments', db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.blog.title}"
