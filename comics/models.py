import datetime
import os
import urllib
import hashlib

from django.core.files.base import ContentFile
from django.db import models


class Comic(models.Model):
    image = models.ImageField(upload_to='comics')
    title = models.CharField(max_length=256)
    slug = models.SlugField()
    date = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)

    date_format = 'F jS, Y'

    @property
    def next(self):
        """Get the next comic by date."""
        try:
            return self.__next
        except AttributeError:
            try:
                # Cache that
                self.__next = Comic.objects.filter(public=True,
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
                self.__previous = Comic.objects.filter(public=True,
                        date__lte=self.date).exclude(pk=self.pk)[0]
                return self.__previous
            except IndexError:
                return None

    def save(self):
        super(Comic, self).save()

        old_name = self.image.name
        base, ext = os.path.splitext(self.image.name)
        name_prefix = os.path.dirname(self.image.name)

        new_name = os.path.join(name_prefix, self.slug + ext)

        contents = self.image.read()

        self.image.save(new_name, ContentFile(contents), save=False)
        self.image.storage.delete(old_name)
        self.image.name = new_name

        super(Comic, self).save()

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

    gravatar_size = 40

    def get_gravatar_url(self, default='identicon'):
        url = 'http://www.gravatar.com/avatar/' + \
                hashlib.md5(self.email.lower()).hexdigest()
        url += '?' + urllib.urlencode({'s': str(self.gravatar_size), 'd':
            default})
        return url

    def get_gravatar_profile_url(self):
        return 'http://www.gravatar.com/' + \
                hashlib.md5(self.email.lower()).hexdigest()

    def get_absolute_url(self):
        return self.comic.get_absolute_url() + '#comment_' + str(self.id)

    class Meta:
        ordering = ['date']
