from django.test import TestCase
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
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])

