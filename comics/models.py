from django.db import models
import datetime

class Comic(models.Model):
    image = models.ImageField(upload_to='comics')
    title = models.CharField(max_length=256)
    date = models.DateTimeField(default=datetime.datetime.now)
    description = models.TextField(blank=True)

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
        return ('comic', [self.pk])

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']
