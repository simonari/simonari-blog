from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    objects = models.Manager()

    STATUS_CHOICES = (
        ('drafted', 'Drafted'),
        ('posted', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='posted')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='drafted')

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        view_name = None
        if self.status == 'drafted':
            view_name = 'blog:draft_detail'
        elif self.status == 'posted':
            view_name = 'blog:post_detail'

        if not view_name:
            raise ValueError(f"No such viewname as {view_name}")

        return reverse(view_name,
                       args=(self.published.year,
                             self.published.month,
                             self.published.day,
                             self.slug))
