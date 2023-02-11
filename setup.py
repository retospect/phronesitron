from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='phronesitron',
   version='0.0.8',
   description='Commandline tool to request help from ML systems',
   long_description=long_description,
   author='Reto Stamm',
   author_email='phronesitron@retostamm.com',
   packages=['phronesitron'],  
   url="https://github.com/retospect/phronesitron",
   install_requires=['wheel', 'openai', 'argparse', 'datetime', 
                     'pyperclip', 'pdfminer.six', 'termcolor'], 
   scripts=['phronesitron/ph', 'phronesitron/paper2txt']
)

