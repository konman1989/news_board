from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete

from .signals_handlers import post_votes_decrement, post_votes_increment

class Post(models.Model):
    title = models.CharField(max_length=128)
    link = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='posts')

    def __str__(self):
        return f"Post by {self.author.full_name}"

    def increment_votes(self):
        self.upvotes += 1
        self.save()

    def decrement_votes(self):
        self.upvotes -= 1
        self.save()


class Comment(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='comments')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')

    def __str__(self):
        return f"Comment to post {self.post.pk}"


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='votes',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name='votes',
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')


post_save.connect(post_votes_increment, sender=Vote)

post_delete.connect(post_votes_decrement, sender=Vote)