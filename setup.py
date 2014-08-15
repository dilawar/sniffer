import os
import sys

from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

configDir = os.path.join(os.environ['HOME'], '.config', 'sniffer')
if not os.path.isdir(configDir):
    print("++ Creating {}".format(configDir))
    os.makedirs(configDir)

setup(
        name='code-sniffer'
        , version='0.9.8'
        , description='A command-line tool to check plagiarim in text and pdf'
        , long_description= read('README.rst') 
        , url = 'https://dilawar.github.io/sniffer'
        , license = 'LGPL'
        , author = 'Dilawar Singh'
        , author_email = 'dilawars@ncbs.res.in'
        , maintainer = 'Dilawar Singh'
        , maintainer_email = 'dilawars@ncbs.res.in'
        , requires = ['Python (>=2.6)']
        , install_requires = [  "pdfminer" ]
        , packages=['sniffer' ]
        , include_package_data = True
        , data_files = [(configDir, ['config'])]
        , classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Environment :: Console',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            ],
        entry_points="""
        [console_scripts]
        code-sniffer=sniffer.main:main
        """
        )


