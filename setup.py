from setuptools import setup, find_packages
from setuptools.command.test import test

def run_tests(self):
    from setuptest.runtests import runtests
    return runtests(self)
test.run_tests = run_tests

setup(
    name='django-publisher',
    version='0.0.2',
    description='Django external publishing app.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    packages = find_packages(),
    test_suite="publisher.tests",
    tests_require=[
        'django-setuptest',
    ],
    #dependency_links = [
    #    'http://github.com/sciyoshi/pyfacebook/tarball/master#egg=pyfacebook',
    #],
    #install_requires = [
    #    'pyfacebook',
    #],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
