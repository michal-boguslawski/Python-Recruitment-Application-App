import pytest
from django.contrib.auth.models import User
from apps.users.models import UserProfile, SiteLinks


@pytest.mark.django_db
@pytest.fixture
def create_user():
    def make_user(
        username: str = "jan",
        email: str = "jan@example.com",
        password: str = "test123"
    ):
        return User(username=username, email=email, password=password)
    return make_user


@pytest.mark.django_db
class TestUserUnit:
    pytestmark = pytest.mark.django_db(transaction=False)

    def test_single_user_created(self, create_user):
        user = create_user("jan", "jan@example.com")
        assert user.username == "jan"
        assert user.email == "jan@example.com"

    def test_multiple_users_created(self, create_user):
        user1 = create_user("jan", "jan@example.com")
        user2 = create_user("anna", "anna.example.com")
        assert user1.username != user2.username
        assert user1.email != user2.email


@pytest.mark.django_db
class TestUserProfileUnit:
    pytestmark = pytest.mark.django_db(transaction=False)

    def test_user_profile_str(self, create_user):
        user = create_user("jan", "jan@example.com")
        profile = UserProfile(user=user)
        assert str(profile) == f"{user.username}'s Profile"

    def test_user_profile_unit(self, create_user):
        user = create_user("jan", "jan@example.com")
        profile1 = UserProfile(user=user)
        profile2 = UserProfile(user=user)
        assert profile1.user == user
        assert profile2.user == user


@pytest.mark.django_db
class TestSiteLinksUnit:
    pytestmark = pytest.mark.django_db(transaction=False)

    def test_sitelinks_str(self, create_user):
        user = create_user("jan", "jan@example.com")
        sitelink = SiteLinks(user=user, name="MySite", url="https://example.com")
        assert str(sitelink) == f"{sitelink.name} - {user.username}"

    def test_sitelinks_unique_url(self, create_user):
        user = create_user("jan", "jan@example.com")
        sitelink1 = SiteLinks(user=user, name="MySite", url="https://example.com")
        sitelink2 = SiteLinks(user=user, name="AnotherSite", url="https://example.com")
        assert sitelink1.url == sitelink2.url
        assert sitelink1.name != sitelink2.name
        assert sitelink1.user == sitelink2.user
        assert sitelink1 != sitelink2

    def test_sitelinks_different_urls(self, create_user):
        user = create_user("jan", "jan@example.com")
        sitelink1 = SiteLinks(user=user, name="MySite", url="https://example.com")
        sitelink2 = SiteLinks(user=user, name="AnotherSite", url="https://another.com")
        assert sitelink1.url != sitelink2.url
        assert sitelink1.name != sitelink2.name
        assert sitelink1.user == sitelink2.user
        assert sitelink1 != sitelink2

    def test_sitelinks_different_users_same_url(self, create_user):
        user1 = create_user("jan", "jan@example.com")
        user2 = create_user("anna", "anna@example.com")
        sitelink1 = SiteLinks(user=user1, name="MySite", url="https://example.com")
        sitelink2 = SiteLinks(user=user2, name="AnotherSite", url="https://example.com")
        assert sitelink1.url == sitelink2.url
        assert sitelink1.name != sitelink2.name
        assert sitelink1.user != sitelink2.user
        assert sitelink1 != sitelink2

    def test_sitelinks_optional_description_unit(self, create_user):
        user = create_user("jan", "jan@example.com")
        sitelink = SiteLinks(
            user=user,
            name="MySite",
            url="https://example.com",
            description=""
        )
        assert sitelink.description == ""
        assert sitelink.name == "MySite"
        assert sitelink.url == "https://example.com"
        assert sitelink.user == user
