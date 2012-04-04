# -*- encoding: utf8 -*-
from setuptools import setup, find_packages

import os

setup(
    name = "django-admin-customizer",
    version = "0.2",
    url = 'https://github.com/ionelmc/django-admin-customizer',
    download_url = '',
    license = 'BSD',
    description = "Django admin customizing interface",
    long_description = file(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author = 'Ionel Cristian Mărieș',
    author_email = 'contact@ionelmc.ro',
    packages = find_packages('src'),
    package_dir = {'':'src'},
    include_package_data = True,
    install_requires = [
        'Django',
    ],
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
