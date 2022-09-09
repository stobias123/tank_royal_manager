import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import sys

setup(name='tank-royal-manager',
      version='0.1.0',
      description='Python bindings to tank-royal games',
      url='',
      author='TOBYYYYYY',
      author_email='stobias123@gmail.com',
      license='',
      packages=['manager', "robocode_event_models"],
)