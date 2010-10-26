from setuptools import setup, find_packages

setup(
    name='django-publisher',
    version='dev',
    description='Django targeted publishing through view layouts and widgets app.',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    url='https://github.com/praekelt/django-publisher',
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False,
)
