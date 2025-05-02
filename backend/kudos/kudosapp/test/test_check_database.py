from django.conf import settings


def test_show_db_name():
    print("Using database file:", settings.DATABASES['default']['NAME'])
