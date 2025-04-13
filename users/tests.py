from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from django.contrib.auth import get_user
from unittest.mock import patch

# Create your tests here.

class RegisterTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('register'),
            data = {
                'username':'tester1',
                'first_name':'testerbek',
                'last_name':'testerov',
                'email':'tester1@gmail.com',
                'password':'tester123',
                'confirm_password':'tester123'
            }
        )
        user = CustomUser.objects.get(username='tester1')
        self.assertEqual(user.username,'tester1')
        self.assertEqual(user.first_name,'testerbek')
        self.assertEqual(user.last_name,'testerov')
        self.assertEqual(user.email,'tester1@gmail.com')
        self.assertNotEqual(user.password,'tester123')
        self.assertTrue(user.check_password('tester123'))
    
    def test_required_fields(self):
        response = self.client.post(
            reverse('register'),
            data = {
                'first_name':'testerbek',
                'last_name':'testerov',
                'email':'tester1@gmail.com'
            }
        )
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('username',form.errors)
        self.assertIn('password',form.errors)
        self.assertIn('confirm_password',form.errors)

    def test_invalid_email(self):
        response = self.client.post(
            reverse('register'),
            data = {
                'username':'tester1',
                'first_name':'testerbek',
                'last_name':'testerov',
                'email':'invelid format',
            }
        )

        form = response.context['form']

        self.assertFalse(form.is_valid())
        self.assertIn('email',form.errors)
    
    def test_unique_username(self):
        self.client.post(
            reverse('register'),
            data = {
                'username':'tester',
                'first_name':'testerbek1',
                'last_name':'testerov1',
                'email':'tester1@gmail.com',
                'password':'tester123',
                'confirm_password':'tester123'
            }
        )
        response = self.client.post(
            reverse('register'),
            data = {
                'username':'tester',
                'first_name':'testerbek2',
                'last_name':'testerov2',
                'email':'tester2@gmail.com',
                'password':'tester123',
                'confirm_password':'tester123'
            }
        )

        form = response.context['form']

        self.assertFalse(form.is_valid())
        self.assertIn('username',form.errors)
        self.assertEqual(form.errors['username'][0],'A user with that username already exists.')
        self.assertEqual(CustomUser.objects.filter(username='tester').count(),1)


class LoginTestCase(TestCase):
    def setUp(self):
        self.new_user = CustomUser.objects.create(username='tester1',first_name='testerbek',last_name='testerov',email='tester1@gmail.com',)
        self.new_user.set_password('tester123')
        self.new_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse('login'),
            data = {
                'username':'tester1',
                'password':'tester123'
            }
        )

        success_user = get_user(self.client)
        self.assertTrue(success_user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('login'),
            data = {
                "username":'wrongusername',
                'password':"Azizbek1410"
            }
        )

        invalid_user = get_user(self.client)
        self.assertFalse(invalid_user.is_authenticated)

        self.client.post(
            reverse('login'),
            data = {
                "username":'tester1',
                'password':"wrongpassword"
            }
        )

        invalid_user2 = get_user(self.client)
        self.assertFalse(invalid_user2.is_authenticated)

        self.client.post(
            reverse('login'),
            data = {
                "username":'wrongusername',
                'password':"wrongpassword"
            }
        )

        invalid_user3 = get_user(self.client)
        self.assertFalse(invalid_user3.is_authenticated)


class LogoutTestCase(TestCase):
    def test_successfully_logout(self):
        response = self.client.post(
            reverse('logout'),
        )

        user = get_user(self.client)
        self.assertEqual(response.status_code,302)
        self.assertFalse(user.is_authenticated)


class PasswordChangeTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='tester1', email='tester1@gmail.com')
        self.user.set_password('tester123')
        self.user.save()

        self.client.login(username='tester1', password='tester123')

    def test_successfully_changed_password(self):
        response = self.client.post(
            reverse('password_change'),
            data={
                'old_password': 'tester123',
                'new_password1': 'tester321',
                'new_password2': 'tester321'
            }
        )

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('tester321'))
        self.assertEqual(response.status_code, 302)

    def test_wrong_old_password(self):
        response = self.client.post(
            reverse('password_change'),
            data={
                'old_password': 'wrongpassword',
                'new_password1': 'tester321',
                'new_password2': 'tester321'
            }
        )

        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('tester321'))


class PasswordChangeDoneTestCase(TestCase):
    def test_password_change_done_view(self):
        response = self.client.get(
            reverse('password_change_done')
        )

        self.assertContains(response,'Endi yangi parolingiz bilan tizimga kirishingiz mumkin.')


class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='tester1',email='tester1@gmail.com')
        self.user.set_password('tester123')
        self.user.save()

    def test_password_reset_email_if_user_is_exists(self):
        response = self.client.post(
            reverse('password_reset'),
            data = {
                "email":'tester1@gmail.com'
            }
        )
        self.assertRedirects(response,reverse('password_reset_done'))
        self.assertEqual(response.status_code,302)

    
    @patch('users.views.send_email_task.delay')
    def test_password_reset_email_not_sent_if_user_does_not_exist(self, mock_send_email):
        response = self.client.post(
            reverse('password_reset'), 
            data={
            'email': 'notfound@gmail.com'
            }
        )
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertFalse(mock_send_email.called)


class PasswordResetDoneTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='tester1',email='tester1@gmail.com')
        self.user.set_password('tester123')
        self.user.save()

    def test_password_reset_view(self):
        response = self.client.get(
            reverse('password_reset_done'),
        )

        self.assertContains(response,'Parolni tiklash uchun email yuborildi')


from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from unittest.mock import patch
from users.models import CustomUser


class PasswordResetConfirmViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='tester1', email='tester1@gmail.com')
        self.user.set_password('oldpassword')
        self.user.save()

        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('password_reset_confirm', args=[self.uidb64, self.token])

    @patch('users.views.send_email_task.delay')
    def test_password_reset_success(self, mock_send_email):
        response = self.client.post(self.url, data={
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
        self.assertRedirects(response, reverse('password_reset_complete'))
        self.assertTrue(mock_send_email.called)

    def test_invalid_token(self):
        invalid_url = reverse('password_reset_confirm', args=[self.uidb64, 'invalid-token'])

        response = self.client.post(invalid_url, data={
            'password1': 'somepass123',
            'password2': 'somepass123'
        }, follow=True)

        self.assertContains(response, 'Havola yaroqsiz yoki eskirgan')


class PasswordResetCompleteTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='tester1',email='tester1@gmail.com')
        self.user.set_password('tester123')
        self.user.save()

    def test_password_reset_complete_view(self):
        response = self.client.get(
            reverse('password_reset_complete'),
        )

        self.assertContains(response,'Parol muvaffaqiyatli tiklandi!')