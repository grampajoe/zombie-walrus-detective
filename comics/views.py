from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from comics.models import Comic

# Create your views here.
def comic(request, comic_id=None, lookup='slug'):
    try:
        latest_comic = Comic.objects.all()[0]
        first_comic = Comic.objects.all().reverse()[0]
    except IndexError:
        latest_comic = None
        first_comic = None
    if comic_id is not None:
        if lookup == 'slug':
            comic = get_object_or_404(Comic, slug=comic_id)
        else:
            comic = get_object_or_404(Comic, pk=comic_id)
            return redirect(comic)
    else:
        comic = latest_comic
    return render_to_response('comics/comic_detail.html', {'comic': comic,
            'latest_comic': latest_comic, 'first_comic': first_comic},
            context_instance=RequestContext(request))

def archive(request):
    comics = Comic.objects.all()
    return render_to_response('comics/archive.html', {'comics': comics},
            context_instance=RequestContext(request))

class ComicRSS(Feed):
    title = 'Zombie Walrus Detective'
    description = 'Zombie Walrus Detective, a webcomic.'
    link = 'http://zombiewalrusdetective.com'
    description_template = 'feed/description.html'
    feed_type = feedgenerator.Rss201rev2Feed

    def items(self):
        return Comic.objects.all()

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date

class ComicAtom(ComicRSS):
    feed_type = feedgenerator.Atom1Feed
    subtitle = ComicRSS.description
