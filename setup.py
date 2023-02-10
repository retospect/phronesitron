from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='phronesitron',
   version='0.0.7',
   description='Commandline tool to request help from ML systems',
   author='Reto Stamm',
   author_email='phronesitron@retostamm.com',
   packages=['phronesitron'],  
   url="https://github.com/retospect/phronesitron",
   install_requires=['wheel', 'openai', 'argparse', 'datetime', 'pyperclip', 'pdfminer.six'], 
   scripts=['phronesitron/ph', 'phronesitron/paper2txt']
)

