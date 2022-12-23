from django.test import Client, TestCase
from http import HTTPStatus
from ..models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='User')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание тестовой группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            id=7,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create_redirect_anonymous_on_admin_login(self):
        """Проверка на редирект неавторизованного пользователя"""
        response = self.guest_client.get("/create/")
        self.assertRedirects(response, "/auth/login/?next=/create/")

    def test_post_edit_is_available_only_author(self):
        """Проверяем, что редактирование поста доступно только автору"""
        self.user = User.objects.get(username=self.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.get(f"/posts/{self.post.id}/edit/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/User/': 'posts/profile.html',
            '/posts/7/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            '/posts/7/edit/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_working_correct(self):
        """Проверка доступности адресов"""
        urls = {
            '/': HTTPStatus.OK,
            '/group/test-slug/': HTTPStatus.OK,
            '/profile/User/': HTTPStatus.OK,
            '/posts/7/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
            '/posts/7/edit/': HTTPStatus.OK,
        }
        for address, status in urls.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, status)
