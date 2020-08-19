# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

import sys

long_desc = '''
Breathe is an extension to reStructuredText and Sphinx to be able to read and
 render `Doxygen <http://www.doxygen.org>`__ xml output.
'''

requires = ['Sphinx>=3.0,<3.3', 'docutils>=0.12', 'six>=1.9']

if sys.version_info < (3, 5):
    print('ERROR: Sphinx requires at least Python 3.5 to run.')
    sys.exit(1)


setup(
    name='breathe',
    version='4.20.0',
    url='https://github.com/michaeljones/breathe',
    download_url='https://github.com/michaeljones/breathe',
    license='BSD',
    author='Michael Jones',
    author_email='m.pricejones@gmail.com',
    description='Sphinx Doxygen renderer',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'breathe-apidoc = breathe.apidoc:main',
        ],
    },
    install_requires=requires,
)
