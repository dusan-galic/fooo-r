import os

from split_settings.tools import include, optional

from food_r.settings.consts import DEVELOPMENT_ENV

ENV = os.getenv("DJANGO_ENV", DEVELOPMENT_ENV)

base_settings = [
    "components/common.py",
    "components/database.py",
    "components/authentication.py",
    "environments/%s.py" % ENV,
    optional("environments/local_settings.py"),
]

include(*base_settings)
