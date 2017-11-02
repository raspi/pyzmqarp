# -*- encoding: utf8 -*-

import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

classifiers = [
    "Programming Language :: Python",
]

requires = [
    'asyncio',
    'zmq',
    'pyroute2',
]

tests_require = [
]

testing_extras = tests_require + [
    'nose',
    'coverage',
    'virtualenv',
]

setup(author=u'Pekka Järvinen',
      name='pyzmqarp',
      version='0.0.1',
      description='ARP events to zmq',
      long_description='Listen on ',
      classifiers=classifiers,
      author_email='',
      url='https://',
      keywords='python pyroute2 arp ',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )
