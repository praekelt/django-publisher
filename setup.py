from setuptools import setup, find_packages

setup(
    name='django-publisher',
    version='dev',
    description='Django external publishing app.',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    url='https://github.com/praekelt/django-publisher',
    packages = find_packages(),
    dependency_links = ['http://github.com/sciyoshi/pyfacebook/tarball/master#egg=pyfacebook',],
    install_requires = ['pyfacebook',],
    include_package_data=True,
)
