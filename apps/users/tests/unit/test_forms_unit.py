import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from io import BytesIO
from PIL import Image

from apps.users.forms import CustomUserCreationForm, \
    CustomUpdateUserForm, UserProfileUpdateForm, SiteLinksForm


@pytest.mark.django_db
class TestCustomUserCreationFormUnit:
    pytestmark = pytest.mark.django_db(transaction=False)

    def test_form_valid_data(self):
        # without database connection
        form_data = {
            'username': 'janedoe',
            'email': 'jane.doe@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '+1234567890',
            'country': 'USA',
            'city': 'New York',
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()

    def test_authenticate(self):
        # mock authenticate to simulate a successful login
        with patch('django.contrib.auth.authenticate') as mock_auth:
            mock_auth.return_value = True  # simulate user found
            result = mock_auth(username='janedoe', password='strongpassword123')
            mock_auth.assert_called_once_with(
                username='janedoe',
                password='strongpassword123'
            )
            assert result is True

    def test_form_invalid_data(self):
        form_data = {
            'username': 'janedoe',
            'email': 'invalid-email',
            'password1': 'strongpassword123',
            'password2': 'differentpassword',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': 'not-a-phone-number',
            'country': 'USA',
            'city': 'New York',
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors
        assert 'password2' in form.errors

    def test_form_missing_required_fields(self):
        form_data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'username' in form.errors
        assert 'email' in form.errors
        assert 'password1' in form.errors
        assert 'password2' in form.errors


@pytest.mark.django_db
class TestCustomUpdateUserFormUnit:
    pytestmark = pytest.mark.django_db(transaction=False)

    def test_form_valid_data(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
        }
        form = CustomUpdateUserForm(data=form_data)
        assert form.is_valid()


@pytest.mark.django_db
class TestUserProfileUpdateFormUnit:
    pytestmark = pytest.mark.django_db(transaction=False)

    def generate_test_image_file(self):
        img = Image.new('RGB', (100, 100), color=(73, 109, 137))
        byte_io = BytesIO()
        img.save(byte_io, 'JPEG')
        byte_io.seek(0)
        return SimpleUploadedFile("test.jpg", byte_io.read(), content_type="image/jpeg")

    def test_form_valid_data_with_image(self):
        image_file = self.generate_test_image_file()
        form_data = {
            'phone_number': '+14155552671',
            'country': 'USA',
            'city': 'New York',
        }
        form_files = {
            'profile_picture': image_file,
        }
        form = UserProfileUpdateForm(data=form_data, files=form_files)
        assert form.is_valid()

    def test_form_valid_data_without_image(self):
        form_data = {
            'phone_number': '+14155552671',
            'country': 'USA',
            'city': 'New York',
        }
        form = UserProfileUpdateForm(data=form_data)
        assert form.is_valid()

    def test_form_invalid_data(self):
        form_data = {
            'phone_number': 'not-a-phone-number',
            'country': '',
            'city': '',
        }
        form = UserProfileUpdateForm(data=form_data)
        assert not form.is_valid()
        assert 'phone_number' in form.errors


@pytest.mark.django_db
class TestSiteLinksFormUnit:
    pytestmark = pytest.mark.django_db(transaction=False)

    def test_form_valid_data(self):
        form_data = {
            'name': 'My Blog',
            'url': 'https://myblog.example.com',
            'description': 'A blog about tech.',
        }
        form = SiteLinksForm(data=form_data)
        assert form.is_valid()

    def test_form_invalid_data(self):
        form_data = {
            'name': '',
            'url': 'not-a-url',
            'description': '',
        }
        form = SiteLinksForm(data=form_data)
        assert not form.is_valid()
        assert 'name' in form.errors
        assert 'url' in form.errors

    def test_form_missing_required_fields(self):
        form_data = {
            'name': '',
            'url': '',
        }
        form = SiteLinksForm(data=form_data)
        assert not form.is_valid()
        assert 'name' in form.errors
        assert 'url' in form.errors
