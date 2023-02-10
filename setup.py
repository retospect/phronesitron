from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='phronesitron',
   version='0.0.2',
   description='Commandline tool to request help from ML systems',
   author='Reto Stamm',
   author_email='phronesitron@retostamm.com',
   packages=['phronesitron'],  
   url="https://github.com/retospect/phronesitron",
   install_requires=['wheel', 'openai', 'argparse', 'datetime', 'pyperlcip'], 
   scripts=['phronesitron/ph']
)

import openai
import os
import sys
import textwrap as tr
import argparse
import time
from termcolor import colored
import datetime
import pyperclip as pc
