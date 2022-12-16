from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовый текст',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.guest_client = Client()


    def test_from_create_authorised_clent(self):
        '''Проверка что форма создает запись в базе данных'''
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, '/profile/TestUser/', status_code=302)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=self.group.id,
                author=self.user,
            ).exists()
        )

    def test_from_create_guest_clent(self):
        """Страница по адресу /create/ перенаправит анонимного
        пользователя на страницу логина. Пост в БД не создастся
        """

        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, '/auth/login/?next=/create/')
        self.assertEqual(Post.objects.count(), post_count)

    def test_from_edit_authorised_clent(self):
        '''Проверка что при авторизованном пользователе
        форма редактирования записи в базе данных изменяет запись
        '''
        post_edit = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
        )
        id_post = post_edit.id
        form_data = {
            'text': 'Тестовый текст измененный',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': id_post}),
            data=form_data,
            follow=True
        )
        post_is_edit = Post.objects.get(id=id_post)
        self.assertEqual(post_is_edit.text, 'Тестовый текст измененный')
        self.assertEqual(post_is_edit.group, self.group)

