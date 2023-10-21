# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from autoslug import AutoSlugField

DRAFT = 'draft'
PUBLISHED = 'published'
STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank = True,null = True)
    avatar = models.ImageField(upload_to="profile_pics",blank=True,null=True)
    bio = models.TextField()
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    def __str__(self):
        return str(self.user)
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True, populate_from='title')
    content = models.TextField()
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    datetime = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    love = models.ManyToManyField(User, related_name='loved_posts', blank=True)

    def __str__(self):
        return str(self.author) +  " Blog Title: " + self.title
    
    def get_absolute_url(self):
        return reverse('blogs')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.blog.title}"
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey(Comment, related_name='replies', null=True, blank=True, on_delete=models.SET_NULL)

