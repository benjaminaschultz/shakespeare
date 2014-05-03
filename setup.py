#!/usr/bin/env python
from setuptools import setup

setup(name='shakespeare',
      version='0.1',
      description='Naive bayes literature aggregator',
      author='Benjamin Schultz',
      author_email='benjamin.a.schultz@gmail.com',
      url='https://github.com/benjaminaschultz/shakespeare',
      scripts=['scripts/shakespeare'],
      packages=['shakespeare','shakespeare.content_sources'],
      package_data={'shakespeare':['data/*.dat'],'shakespeare.content_sources':[]},
      license='BSD',
)
