from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel
from django.contrib.humanize.templatetags import humanize
from django.template.defaultfilters import slugify

User = get_user_model()
# Create your models here.


class Room(BaseModel, models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)
    slug = models.SlugField(default=False)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'

    def get_date(self):
        return humanize.naturaltime(self.created_at)


class Message(BaseModel, models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.created_at}]'
    
    def get_date(self):
        return humanize.naturaltime(self.created_at)
