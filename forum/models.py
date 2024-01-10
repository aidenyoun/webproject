from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('notice', '공지사항'),
        ('free', '자유게시판'),
        ('question', '질문게시판'),
        ('review', '후기게시판'),
        ('suggestion', '건의사항'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='free')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    liked_users = models.ManyToManyField(User, related_name='liked_posts', blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recommended_posts = models.ManyToManyField('Post', related_name='recommended_by')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    liked_users = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def is_liked_by_user(self, user):
        return self.liked_users.filter(pk=user.pk).exists()

