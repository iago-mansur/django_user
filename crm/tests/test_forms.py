from django.test import TestCase
from django.contrib.auth.models import User
from crm.forms import CreateUserForm

class CreateUserFormTest(TestCase):

    def test_form_valid_data(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
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
        self.assertEqual(form.errors['username'], ['Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'])

    def test_form_invalid_password(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password',
            'password2': 'password'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['This password is too common.'])
