from django.db import models
import datetime
import os

class Comic(models.Model):
    image = models.ImageField(upload_to='comics')
    title = models.CharField(max_length=256)
    slug = models.SlugField()
    date = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField(blank=True)

    date_format = 'F jS, Y'

    @property
    def next(self):
        """Get the next comic by date."""
        try:
            return self.__next
        except AttributeError:
            try:
                # Cache that
                self.__next = Comic.objects.filter(
                        date__gte=self.date).exclude(pk=self.pk).reverse()[0]
                return self.__next
            except IndexError:
                return None

    @property
    def previous(self):
        """Get the previous comic by date."""
        try:
            return self.__previous
        except AttributeError:
            try:
                # Cache that
                self.__previous = Comic.objects.filter(
                        date__lte=self.date).exclude(pk=self.pk)[0]
                return self.__previous
            except IndexError:
                return None

    @models.permalink
    def get_absolute_url(self):
        return ('comic', [self.slug])

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']

class Comment(models.Model):
    comic = models.ForeignKey(Comic)
    date = models.DateTimeField(default=datetime.datetime.now)
    name = models.CharField(max_length=256)
    email = models.EmailField()
    website = models.URLField(blank=True)
    comment = models.TextField()
    approved = models.BooleanField(default=False)
