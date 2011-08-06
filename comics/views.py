from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from zombiewalrus.comics.models import Comic

# Create your views here.
def comic(request, comic_id=None):
    try:
        latest_comic = Comic.objects.all()[0]
        first_comic = Comic.objects.all().reverse()[0]
    except IndexError:
        latest_comic = None
        first_comic = None
    if comic_id is not None:
        comic = get_object_or_404(Comic, pk=comic_id)
    else:
        comic = latest_comic
    return render_to_response('comics/comic_detail.html', {'comic': comic,
            'latest_comic': latest_comic, 'first_comic': first_comic},
            context_instance=RequestContext(request))

def archive(request):
    comics = Comic.objects.all()
    return render_to_response('comics/archive.html', {'comics': comics},
            context_instance=RequestContext(request))
