# conftest.py
import pytest
import os
from django.conf import settings
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventory_project.settings")  # replace with actual project name

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
@pytest.fixture(scope='session', autouse=True)
def django_setup():
    django.setup()