from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from crm.forms import CreateUserForm

class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crm/register.html')

    def test_register_post_valid(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('login'))  # Ensure this matches the correct view name
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_post_invalid(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser$',
            'email': 'testuser@example.com',
            'password1': 'password',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 200)  # Expecting to stay on the same page
        self.assertTemplateUsed(response, 'crm/register.html')
        self.assertFormError(response, 'form', 'username', 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')
        self.assertFormError(response, 'form', 'password2', 'This password is too common.')

    def test_register_post_missing_fields(self):
        response = self.client.post(self.register_url, {})
        self.assertEqual(response.status_code, 200)  # Expecting to stay on the same page
        self.assertTemplateUsed(response, 'crm/register.html')
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'This field is required.')
        self.assertFormError(response, 'form', 'password1', 'This field is required.')
        self.assertFormError(response, 'form', 'password2', 'This field is required.')

class CreateUserFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='StrongPassword123!')

    def test_form_valid_data(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_username(self):
        form = CreateUserForm(data={
            'username': 'testuser$',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.', form.errors['username'])

    def test_form_invalid_password(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password',
            'password2': 'password'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('This password is too common.', form.errors['password2'])

    def test_form_missing_fields(self):
        form = CreateUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertEqual(form.errors['password2'], ['This field is required.'])

    def test_form_password_mismatch(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'DifferentPassword123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn('The two password fields didn’t match.', form.errors['password2'])

    def test_form_duplicate_email(self):
        form = CreateUserForm(data={
            'username': 'newuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('A user with that email already exists.', form.errors['email'])
