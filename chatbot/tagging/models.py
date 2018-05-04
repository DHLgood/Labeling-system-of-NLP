from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    sentence_start_id = models.IntegerField(default=0)
    sentence_end_id = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username


class Sentence(models.Model):
    last_changed_by = models.ForeignKey(User,on_delete=models.CASCADE)
    last_changed_time = models.DateTimeField(auto_now=True)
    changed_times = models.IntegerField(default=0)
    text = models.TextField(help_text="row text")
    # tokens = models.TextField(blank=True, help_text="json string that token list")
    tokens_and_pos = models.TextField(blank=True, help_text="json object that segment tokens list")
    tagged = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    tag_type = models.CharField(help_text="tag type", default=0,max_length=255)
    file_name = models.CharField(help_text="file_name", default=1,max_length=255)
    primary = (id, 'tag_type')
    def __str__(self):
        return '{:>10}. {}'.format(self.id, self.text)



