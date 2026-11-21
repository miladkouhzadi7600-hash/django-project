from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserAccountTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'StrongPass123!xyz',
            'password2': 'StrongPass123!xyz',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_can_log_in(self):
        User.objects.create_user(username='testuser', password='StrongPass123!xyz')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPass123!xyz',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}"
        )

    def test_user_can_update_profile(self):
        user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!xyz'
        )
        self.client.login(username='testuser', password='StrongPass123!xyz')

        response = self.client.post(reverse('profile'), {
            'first_name': 'Ali',
            'last_name': 'Ahmadi',
            'email': 'ali@example.com',
        })

        self.assertRedirects(response, reverse('profile'))
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Ali')
        self.assertEqual(user.last_name, 'Ahmadi')
        self.assertEqual(user.email, 'ali@example.com')

    def test_logout_rejects_get_request(self):
        user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!xyz'
        )
        self.client.login(username='testuser', password='StrongPass123!xyz')

        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(
            '_auth_user_id' in self.client.session
        )

    def test_user_can_log_out_with_post(self):
        User.objects.create_user(
            username='testuser',
            password='StrongPass123!xyz'
        )
        self.client.login(username='testuser', password='StrongPass123!xyz')

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_password_change_requires_login(self):
        response = self.client.get(reverse('password_change'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('password_change')}"
        )

    def test_user_can_change_password_and_stay_logged_in(self):
        user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!xyz'
        )
        self.client.login(username='testuser', password='StrongPass123!xyz')

        response = self.client.post(reverse('password_change'), {
            'old_password': 'StrongPass123!xyz',
            'new_password1': 'NewStrongPass456!xyz',
            'new_password2': 'NewStrongPass456!xyz',
        })

        self.assertRedirects(response, reverse('profile'))
        user.refresh_from_db()
        self.assertTrue(user.check_password('NewStrongPass456!xyz'))
        self.assertTrue('_auth_user_id' in self.client.session)
