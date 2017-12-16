from django.db import models

from shortener.models import ShortURL


class ClickEventManager(models.Manager):

    def create_event(self, shortInstance):
        if isinstance(shortInstance, ShortURL):
            obj, created = self.get_or_create(short_url=shortInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    short_url = models.OneToOneField(ShortURL, on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)