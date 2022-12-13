from http import HTTPStatus
from django.urls import reverse
from django.test import Client, TestCase


class UserURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_page(self):
        urls = [
            reverse('users:logout'),
            reverse('users:signup'),
            reverse('users:login'),
            reverse('users:password_reset'),
            reverse('users:password_reset_complete'),
            reverse('users:password_reset_form'),
        ]

        for address in urls:
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
