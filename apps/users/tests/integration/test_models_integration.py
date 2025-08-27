import pytest
from django.db import IntegrityError, transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from apps.users.models import UserProfile, SiteLinks


@pytest.fixture
def create_user(db):
    def make_user(username: str, email: str, password: str = "test123"):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
    return make_user


class TestUser:
    @pytest.mark.django_db
    def test_single_user_created(self, create_user):
        user = create_user("jan", "jan@example.com")

        assert user.username == "jan"
        assert user.email == "jan@example.com"

    @pytest.mark.django_db
    def test_multiple_users_created(self, create_user):
        _ = create_user("jan", "jan@example.com")
        _ = create_user("anna", "anna@example.com")

        assert User.objects.count() == 2

    @pytest.mark.django_db
    def test_login_password(self):
        from django.contrib.auth.models import User
        _ = User.objects.create_user(username="jan", password="correctpass")

        result = authenticate(username="jan", password="correctpass")

        assert result is not None

    @pytest.mark.django_db
    def test_login_wrong_password(self):
        from django.contrib.auth.models import User
        _ = User.objects.create_user(username="jan", password="correctpass")

        result = authenticate(username="jan", password="wrongpass")

        assert result is None


class TestUserProfile:
    @pytest.mark.django_db
    def test_user_profile_str(self):
        user = User.objects.create(username="jan", email="jan@example.com")
        profile, created = UserProfile.objects.get_or_create(user=user)

        assert profile.user.username == "jan"
        assert str(profile) == f"{user.username}'s Profile"

    @pytest.mark.django_db
    def test_user_profile_unique(self):
        user = User.objects.create(username="jan", email="jan@example.com")
        profile1, created1 = UserProfile.objects.get_or_create(user=user)
        profile2, created2 = UserProfile.objects.get_or_create(user=user)
        assert profile1 == profile2
        assert UserProfile.objects.count() == 1

    @pytest.mark.django_db
    def test_user_profile_fields(self):
        user = User.objects.create(username="jan", email="jan@example.com")
        profile = UserProfile.objects.create(
            user=user,
            phone_number="+1234567890",
            city="Anytown",
            country="Countryland"
        )
        assert profile.phone_number == "+1234567890"
        assert profile.city == "Anytown"
        assert profile.country == "Countryland"


class TestSiteLinks:
    @pytest.mark.django_db
    def test_user_profile_social_links(self):
        user = User.objects.create(username="jan", email="jan@example.com")
        github_link = SiteLinks(
            user=user,
            name="GitHub",
            url="httsp://github.com/jan"
        )
        linkedin_link = SiteLinks(
            user=user,
            name="LinkedIn",
            url="https://linkedin.com/in/jan"
        )
        SiteLinks.objects.bulk_create([github_link, linkedin_link])
        links = SiteLinks.objects.filter(user=user)
        assert links.count() == 2
        assert links[0].name == "GitHub"
        assert links[1].name == "LinkedIn"

    @pytest.mark.django_db
    def test_user_profile_social_links_str(self):
        user = User.objects.create(username="jan", email="jan@example.com")
        link = SiteLinks.objects.create(
            user=user,
            name="GitHub",
            url="https://github.com/jan"
        )
        assert str(link) == f"{link.name} - {user.username}"

    @pytest.mark.django_db
    def test_user_profile_social_links_unique(self):
        user = User.objects.create(username="jan", email="jan@example.com")
        _ = SiteLinks.objects.create(
            user=user,
            name="GitHub",
            url="https://github.com/jan"
        )
        with transaction.atomic():
            with pytest.raises(IntegrityError):
                _ = SiteLinks.objects.create(
                    user=user,
                    name="GitHub Duplicate",
                    url="https://github.com/jan"
                )
        assert SiteLinks.objects.count() == 1
