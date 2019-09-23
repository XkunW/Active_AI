from distutils.core import setup
import setuptools

import os

source_dir = os.path.dirname(os.path.realpath(__file__))
requirementPath = source_dir + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setup(name='active_ai',
      version='0.1',
      package_dir={'active_ai': 'src/lib'},
      packages=['active_ai'],
      install_requires=install_requires
      )
