"""models.py"""
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    """post model"""
    body = RichTextUploadingField(blank=True, null=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               null=True)
    likes = models.ManyToManyField(to=User,
                                   related_name='likes',
                                   blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(to='Tag',
                                 related_name='tags',
                                 blank=True)
    private = models.BooleanField(default=0)
    private_key = models.CharField(default='public', max_length=32)

    def __str__(self):
        """str function"""
        return self.title

    def get_absolute_url(self):
        """url function"""
        return reverse('blogapp:chat_page', args=[self.id, self.private_key])

    def is_private(self):
        """check if private"""
        return bool(self.private)

    class Meta:
        """meta class"""
        ordering = ['-created']


class Comment(models.Model):
    """comment model"""
    post = models.ForeignKey(to=Post,
                             on_delete=models.CASCADE)
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE)
    content = RichTextUploadingField(blank=True, null=True)
    timestap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """str function"""
        return '{}-{}'.format(self.post.title, str(self.user.username))


class Tag(models.Model):
    """tag model"""
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        """str function"""
        return self.tag_name


class Profile(models.Model):
    """profile model"""
    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE)
    country = models.CharField(max_length=32, blank=True)
    contacts = models.CharField(max_length=64, blank=True)
    image = models.ImageField(upload_to='images', blank=True)



