
from setuptools import setup, find_packages
from kubesecret.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='kubesecret',
    version=VERSION,
    description='Manage Kubernetes secrets',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Ryan Flynn',
    author_email='ryan@narwh.al',
    url='https://github.com/johndoe/myapp/',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'kubesecret': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        kubesecret = kubesecret.main:main
    """,
)
