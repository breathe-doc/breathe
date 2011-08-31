# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup, find_packages

import os
import sys
from distutils import log

import breathe

long_desc = '''
Breathe is an extension to reStructuredText and Sphinx to be able to read and 
render `Doxygen <http://www.doxygen.org>`__ xml output.
'''

requires = ['Sphinx>=1.0.7', 'docutils>=0.5']

if sys.version_info < (2, 4):
    print('ERROR: Sphinx requires at least Python 2.4 to run.')
    sys.exit(1)

if sys.version_info < (2, 5):
    # Python 2.4's distutils doesn't automatically install an egg-info,
    # so an existing docutils install won't be detected -- in that case,
    # remove the dependency from setup.py
    try:
        import docutils
        if int(docutils.__version__[2]) < 4:
            raise ValueError('docutils not recent enough')
    except:
        pass
    else:
        del requires[-1]

    # The uuid module is new in the stdlib in 2.5
    requires.append('uuid>=1.30')




setup(
    name='breathe',
    version=breathe.__version__,
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
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    use_2to3=True,
)
