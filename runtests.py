# /usr/bin/python
import django
import sys

from django.test.runner import DiscoverRunner
from django.conf import settings

settings.configure(
    INSTALLED_APPS=(
        'django_tables2_reports',
    ),
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "TEST": {
                "SERIALIZE": False
            }
        },
    }
)

if __name__ == "__main__":
    django.setup()
    runner = DiscoverRunner()
    failures = runner.run_tests(['django_tables2_reports'])
    if failures:
        sys.exit(failures)
