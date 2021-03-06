from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from django.http import Http404
from django.db.models import Q
from django.core.mail import mail_admins
from comics.models import Comic, Comment
from comics.forms import CommentForm, ContactForm

def comic(request, comic_id=None, lookup='slug'):
    """Show a comic!!!
    
    Comics can be looked up by id or slug, to preserve backwards compatibility.
    If neither are provided, the latest comic will be shown.

    POSTing to one o' these URLs posts a comment. No user accounts are used, so
    posted but unapproved comments are stored in the session, as well as values
    for the name, email, and website fields.
    """
    # If the user is an admin, don't filter out public=False
    if request.user and request.user.is_authenticated() and \
            request.user.is_staff:
        public = {}
    else:
        public = {'public': True}

    # Forget user details
    if request.GET.get('forget', False) is not False:
        request.session['comments_profile'] = {}

    try:
        latest_comic = Comic.objects.filter(**public)[0]
        first_comic = Comic.objects.filter(**public).reverse()[0]
    except IndexError:
        # No comics somehow!
        latest_comic = None
        first_comic = None
    if comic_id is not None:
        if lookup == 'slug':
            comic = get_object_or_404(Comic, slug=comic_id, **public)
        else:
            comic = get_object_or_404(Comic, pk=comic_id, **public)
            return redirect(comic)
    elif latest_comic is not None:
        comic = latest_comic
    else:
        raise Http404

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            name = comment_form.cleaned_data['name']
            email = comment_form.cleaned_data['email']
            website = comment_form.cleaned_data['website']
            comment = comment_form.cleaned_data['comment']

            c = Comment.objects.create(name=name, email=email, website=website,
                    comment=comment, comic=comic)

            # Add comment to session's submitted comments, save user info
            submitted = request.session.get('comments_submitted', [])
            submitted.append(c.pk)
            request.session['comments_submitted'] = submitted
            request.session['comments_profile'] = {'name': name, 'email': email,
                    'website': website}

            # Email to admins
            approve_url = 'http://zombiewalrusdetective.com{0}#comments'.format(
                    comic.get_absolute_url())
            subject = '{0} commented on {1}'.format(name, comic.title)
            message = u'Name: {0}\nEmail: {1}\nWebsite: {2}\nComment: {3}\n\nTo approve/deny: {4}'.format(
                    name, email, website, comment, approve_url)
            mail_admins(subject, message)

            return redirect(comic.get_absolute_url()+'#comment_'+str(c.pk))
    else:
        comment_form = CommentForm(initial=request.session.get('comments_profile', {}))

    if request.user and request.user.is_authenticated() and \
            request.user.is_staff:
        comments = comic.comment_set.all()
    else:
        comments = comic.comment_set.filter(Q(approved=True) |
                Q(pk__in=request.session.get('comments_submitted', [])))

    return render_to_response('comics/comic_detail.html', {'comic': comic,
            'latest_comic': latest_comic, 'first_comic': first_comic,
            'comment_form': comment_form, 'comments': comments},
            context_instance=RequestContext(request))

def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user and request.user.is_authenticated() and \
            request.user.is_staff:
        comment.approved = True
        comment.save()
    return redirect(comment)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user and request.user.is_authenticated() and \
            request.user.is_staff:
        comment.delete()
    return redirect(comment.comic.get_absolute_url() + '#comments')

def archive(request):
    comics = Comic.objects.filter(public=True)
    return render_to_response('comics/archive.html', {'comics': comics},
            context_instance=RequestContext(request))

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            from django.core.mail import EmailMessage

            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            sender = 'zombiewalrusdetective.com' \
                    ' <contact@zombiewalrusdetective.com>'
            subject = '{0} has sent a message!'.format(name)
            body = 'Email: {0}\n\n{1}'.format(email, message)
            recipients = ['joe@zombiewalrusdetective.com']

            email = EmailMessage(subject, body, sender, recipients,
                       headers={'Reply-to': email})
            email.send()

            return redirect('contact_thanks')
    else:
        form = ContactForm()

    return render_to_response('contact.html', {'contact_form': form},
            context_instance=RequestContext(request))

class ComicRSS(Feed):
    title = 'Zombie Walrus Detective'
    description = 'Zombie Walrus Detective, a webcomic.'
    link = 'http://zombiewalrusdetective.com'
    description_template = 'feed/description.html'
    feed_type = feedgenerator.Rss201rev2Feed

    def items(self):
        return Comic.objects.filter(public=True)

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date

class ComicAtom(ComicRSS):
    feed_type = feedgenerator.Atom1Feed
    subtitle = ComicRSS.description
