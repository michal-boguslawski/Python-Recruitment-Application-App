import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

from apps.users.forms import CustomUserCreationForm, \
    CustomUpdateUserForm, UserProfileUpdateForm, SiteLinksForm
from django.contrib.auth.models import User
from apps.users.models import UserProfile, SiteLinks


@pytest.fixture
def create_user(db):
    def make_user(
        username: str = "jan",
        email: str = "jan.kowalski@gmail.com",
        password: str = "test123",
        first_name: str = "",
        last_name: str = ""
    ):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
    return make_user


class TestCustomUserCreationForm:
    @pytest.mark.django_db
    def test_form_valid_data(self):
        form_data = {
            'username': 'jan',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'phone_number': '+48123456789',
            'email': 'jan.kowalski@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'country': 'Countryland',
            'city': 'Anytown'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.username == 'jan'
        assert user.email == 'jan.kowalski@example.com'
        assert user.first_name == 'Jan'
        assert user.last_name == 'Kowalski'
        profile = UserProfile.objects.get(user=user)
        assert profile.phone_number.as_e164 == '+48123456789'
        assert profile.country == 'Countryland'
        assert profile.city == 'Anytown'

    @pytest.mark.django_db
    def test_form_missing_optional_fields(self):
        form_data = {
            'username': 'anna',
            'email': 'jan.kowalski@gmail.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.username == 'anna'
        assert user.email == 'jan.kowalski@gmail.com'
        assert user.first_name == ''
        assert user.last_name == ''
        profile = UserProfile.objects.get(user=user)
        assert profile.phone_number == ''
        assert profile.country == ''
        assert profile.city == ''
        assert not profile.profile_picture
        assert str(profile) == "anna's Profile"
        assert UserProfile.objects.count() == 1
        assert User.objects.count() == 1

    @pytest.mark.django_db
    def test_form_invalid_password_mismatch(self):
        form_data = {
            'username': 'jan',
            'email': 'jan.kowalski@gmail.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'password2' in form.errors
        assert form.errors['password2'] == ["The two password fields didn’t match."]
        assert User.objects.count() == 0

    @pytest.mark.django_db
    def test_form_invalid_duplicate_username(self, create_user):
        _ = create_user()
        form_data = {
            'username': 'jan',
            'email': 'jan.kowalski@gmail.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'username' in form.errors
        assert form.errors['username'] == ["A user with that username already exists."]
        assert User.objects.count() == 1
        assert UserProfile.objects.count() == 0

    @pytest.mark.django_db
    def test_form_invalid_duplicate_email(self, create_user):
        _ = create_user()
        form_data = {
            'username': 'anna',
            'email': 'jan.kowalski@gmail.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors
        assert form.errors['email'] == ["A user with that email already exists."]
        assert User.objects.count() == 1
        assert UserProfile.objects.count() == 0

    @pytest.mark.django_db
    def test_form_image_field(self):
        # generate a simple image file
        size = (800, 600)
        storage = BytesIO()
        img = Image.new("RGB", size)
        img.save(storage, "JPEG")
        storage.seek(0)
        image = SimpleUploadedFile(
            name='test.jpg',
            content=storage.getvalue(),
            content_type='image/jpeg'
        )
        form_data = {
            'username': 'jan',
            'email': 'jan.kowalski@gmail.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'profile_picture': image
        }
        form = CustomUserCreationForm(data=form_data, files={'profile_picture': image})
        assert form.is_valid(), form.errors
        user = form.save()
        profile = UserProfile.objects.get(user=user)
        assert profile.profile_picture is not None

    @pytest.mark.django_db
    def test_form_name_capitalization(self):
        form_data = {
            'username': 'jan',
            'first_name': 'jaN',
            'last_name': 'kOWALski',
            'email': 'jan.kowalski@gmail.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.first_name == 'Jan'
        assert user.last_name == 'Kowalski'


class TestUserProfileUpdateForm:
    @pytest.mark.django_db
    def test_form_valid_data(self, create_user):
        user = create_user()
        form_data = {
            'phone_number': '+48123456789',
            'country': 'Countryland',
            'city': 'Anytown'
        }
        _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'phone_number': '',
                'country': '',
                'city': ''
            }
        )[0]
        form = UserProfileUpdateForm(data=form_data, instance=user.userprofile)
        assert form.is_valid()
        profile = form.save()
        assert profile.phone_number.as_e164 == '+48123456789'
        assert profile.country == 'Countryland'
        assert profile.city == 'Anytown'

    @pytest.mark.django_db
    def test_form_missing_optional_fields(self, create_user):
        user = create_user()
        _ = UserProfile.objects.create(
            user=user,
            phone_number='+48123456789',
            country='Countryland',
            city='Anytown'
        )
        form_data = {}
        form = UserProfileUpdateForm(data=form_data, instance=user.userprofile)
        assert form.is_valid()
        profile = form.save()
        assert profile.phone_number == '+48123456789'
        assert profile.country == 'Countryland'
        assert profile.city == 'Anytown'
        assert not profile.profile_picture
        assert str(profile) == "jan's Profile"
        assert UserProfile.objects.count() == 1
        assert User.objects.count() == 1


class TestCustomUpdateUserForm:
    @pytest.mark.django_db
    def test_form_valid_data(self, create_user):
        user = create_user()
        form_data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski'
        }
        form = CustomUpdateUserForm(data=form_data, instance=user)
        assert form.is_valid()
        updated_user = form.save()
        assert updated_user.first_name == 'Jan'
        assert updated_user.last_name == 'Kowalski'

    @pytest.mark.django_db
    def test_form_missing_optional_fields(self, create_user):
        user = create_user(first_name='Jan', last_name='Kowalski')
        form_data = {}
        form = CustomUpdateUserForm(data=form_data, instance=user)
        assert form.is_valid()
        updated_user = form.save()
        assert updated_user.first_name == 'Jan'
        assert updated_user.last_name == 'Kowalski'

    @pytest.mark.django_db
    def test_form_name_capitalization(self, create_user):
        user = create_user()
        form_data = {
            'first_name': 'jaN',
            'last_name': 'kOWALski'
        }
        form = CustomUpdateUserForm(data=form_data, instance=user)
        assert form.is_valid()
        updated_user = form.save()
        assert updated_user.first_name == 'Jan'
        assert updated_user.last_name == 'Kowalski'


class TestSiteLinksForm:
    @pytest.mark.django_db
    def test_form_valid_data(self, create_user):
        user = create_user()
        form_data = {
            'name': 'GitHub',
            'url': 'https://github.com/jan',
            'description': 'My GitHub profile',
        }
        form = SiteLinksForm(data=form_data)
        assert form.is_valid()
        link = form.save(commit=False)
        link.user = user
        link.save()
        assert link.name == 'GitHub'
        assert link.url == 'https://github.com/jan'
        assert link.description == 'My GitHub profile'
        assert link.user == user
        assert str(link) == f"{link.name} - {user.username}"

    @pytest.mark.django_db
    def test_form_missing_optional_fields(self, create_user):
        user = create_user()
        form_data = {
            'name': 'GitHub',
            'url': 'https://github.com/jan',
        }
        form = SiteLinksForm(data=form_data)
        print(form.errors)
        assert form.is_valid()
        link = form.save(commit=False)
        link.user = user
        link.save()
        assert link.name == 'GitHub'
        assert link.url == 'https://github.com/jan'
        assert link.description == ''
        assert link.user == user
        assert str(link) == f"{link.name} - {user.username}"
        assert SiteLinks.objects.count() == 1
        assert User.objects.count() == 1

    @pytest.mark.django_db
    def test_form_invalid_duplicate_url(self, create_user):
        user = create_user()
        _ = SiteLinks.objects.create(
            user=user,
            name='GitHub',
            url='https://github.com/jan'
        )
        form_data = {
            'name': 'GitHub Duplicate',
            'url': 'https://github.com/jan',
            'description': 'Duplicate link',
        }
        form = SiteLinksForm(data=form_data)
        assert not form.is_valid()
        assert 'url' in form.errors
        assert form.errors['url'] == ["Site links with this Url already exists."]
        assert SiteLinks.objects.count() == 1
        assert User.objects.count() == 1

    @pytest.mark.django_db
    def test_form_invalid_url_format(self, create_user):
        _ = create_user()
        form_data = {
            'name': 'GitHub',
            'url': 'not-a-valid-url',
            'description': 'Invalid URL format',
        }
        form = SiteLinksForm(data=form_data)
        assert not form.is_valid()
        assert 'url' in form.errors
        assert form.errors['url'] == ["Enter a valid URL."]
        assert SiteLinks.objects.count() == 0
        assert User.objects.count() == 1

    @pytest.mark.django_db
    def test_form_name_length_exceeded(self, create_user):
        _ = create_user()
        form_data = {
            'name': 'G' * 51,  # Exceeds max_length of 50
            'url': 'https://github.com/jan',
            'description': 'Name too long',
        }
        form = SiteLinksForm(data=form_data)
        assert not form.is_valid()
        assert 'name' in form.errors
        assert form.errors['name'] == [
            "Ensure this value has at most 50 characters (it has 51)."
        ]
        assert SiteLinks.objects.count() == 0
        assert User.objects.count() == 1

    @pytest.mark.django_db
    def test_multiple_social_links(self, create_user):
        user = create_user()
        links_data = [
            {
                'name': 'GitHub',
                'url': 'https://github.com/jan',
                'description': 'My GitHub profile',
            },
            {
                'name': 'LinkedIn',
                'url': 'https://linkedin.com/in/jan',
                'description': 'My LinkedIn profile',
            }
        ]
        for data in links_data:
            form = SiteLinksForm(data=data)
            assert form.is_valid()
            link = form.save(commit=False)
            link.user = user
            link.save()
        links = SiteLinks.objects.filter(user=user)
        assert links.count() == 2
        assert links[0].name == 'GitHub'
        assert links[1].name == 'LinkedIn'
        assert str(links[0]) == f"{links[0].name} - {user.username}"
        assert str(links[1]) == f"{links[1].name} - {user.username}"
        assert SiteLinks.objects.count() == 2
        assert User.objects.count() == 1
