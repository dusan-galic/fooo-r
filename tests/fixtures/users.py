import pytest
from freezegun import freeze_time


@pytest.fixture
@freeze_time("2024-01-01 22:00:00")
def user1(django_user_model):
    user = django_user_model.objects.create(
        email="testara.testic@test.com",
        first_name="Testara",
        last_name="Testic",
    )
    return user


@pytest.fixture
@freeze_time("2024-01-01 22:00:00")
def user2(django_user_model):
    user = django_user_model.objects.create(
        email="testara2.testic2@test.com",
        first_name="Testara2",
        last_name="Testic2",
    )
    return user
