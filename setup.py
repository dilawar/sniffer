import os

from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
        name='code-sniffer'
        , version='0.9.7'
        , description='A command-line tool to check plagiarim in text and pdf'
        , long_description= read('README.rst') 
        , url = 'https://dilawar.github.io/sniffer'
        , licence = 'GNU-GPL'
        , author = 'Dilawar Singh'
        , author_email = 'dilawars@iitb.ac.in'
        , maintainer = 'Dilawar Singh'
        , maintainer_email = 'dilawars@iitb.ac.in'
        , requires = ['Python (>=2.6)']
        , install_requires = { "pdfminer"}
        , packages=['sniffer' ]
        , include_package_data = True
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


