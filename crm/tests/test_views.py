from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

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