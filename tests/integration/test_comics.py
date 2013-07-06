"""
Tests for the comics app
"""
from django.test import TestCase

from comics.models import Comic


class ComicTest(TestCase):
    """Tests for the comic view."""
    fixtures = ['tests/integration/comics_data.json']

    def test_unicode_comment(self):
        """Test posting a comment with unicode characters."""
        comic = Comic.objects.get(id=1)

        data = {
            'name': 'Test Guy',
            'email': 'test@example.com',
            'website': 'http://www.test.com',
            'comment': '\xe2\x84\x9cuh roh!',
        }

        response = self.client.post(comic.get_absolute_url(), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(data['comment'], response.content)
