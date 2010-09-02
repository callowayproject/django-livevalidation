from setuptools import setup, find_packages

setup(
    name = "django-livevalidation",
    version = '0.1.1',
    url = 'http://github.com/washingtontimes/django-livevalidation',
    author = 'Justin Quick',
    author_email = 'justquick@gmail.com',
    description = 'Live validation for Django forms. It validates as you type. Uses scripts from livevalidation.com',
    packages = find_packages(),
    include_package_data = True,
)
