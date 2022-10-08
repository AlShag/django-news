import datetime

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from rest_framework.test import APITestCase

from .models import News, Tag


class NewsViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        cls.tag = Tag.objects.create(
            name='name',
        )
        cls.news = News.objects.create(
            title='title',
            body='paragraph',
        )
        cls.news.tags.add(cls.tag)

    def test_news_list(self) -> None:
        self.client.force_authenticate(self.superuser)
        url = reverse('news-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_news_retrieve(self) -> None:
        self.client.force_authenticate(self.superuser)
        url = reverse('news-detail', kwargs={'pk': self.news.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(self.news.views_count, 1)

    def test_news_create(self) -> None:
        self.client.force_authenticate(self.superuser)
        url = reverse('news-list')
        response = self.client.post(
            url,
            {
                'title': 'custom_title',
                'body': 'paragraph',
                'thumbnail': SimpleUploadedFile(
                    name='test_image.jpg',
                    content=open('static/github.png', 'rb').read(),
                    content_type='image/png'),
            }
        )
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_news_destroy(self) -> None:
        self.client.force_authenticate(self.superuser)
        url = reverse('news-detail', kwargs={'pk': self.news.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


class PagesTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        cls.tag = Tag.objects.create(
            name='name',
        )
        cls.news = News.objects.create(
            title='title',
            body='paragraph',
            thumbnail=SimpleUploadedFile(
                name='test_image.jpg',
                content=open('static/github.png', 'rb').read(),
                content_type='image/png'
            ),
        )
        cls.news.tags.add(cls.tag)

    def test_news_list_page(self) -> None:
        url = reverse('news_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_news_detail_page(self) -> None:
        url = reverse('news_detail', kwargs={'pk': self.news.pk})
        self.assertEqual(self.news.views_count, 0)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(self.news.views_count, 1)
        self.client.get(url)
        self.assertEqual(self.news.views_count, 1)

    def test_get_news_list_by_tag(self):
        url = reverse('news_by_tag', kwargs={'pk': self.tag.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_views_stats(self) -> None:
        url = reverse('stats')
        response = self.client.post(url, data={
            'from_date': datetime.datetime.today() - datetime.timedelta(days=7),
            'to_date': datetime.datetime.today()
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
