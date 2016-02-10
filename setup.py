#!/usr/bin/env python

from setuptools import setup

# http://pypi.python.org/pypi?%3Aaction=list_classifiers

setup(
    name='Lepsius',
    version='0.0.1',
    author='Mathieu Lecarme',
    author_email='mathieu@garambrogne.net',
    url='https://github.com/bearstech/lepsius',
    description="Reads live log.",
    packages=['lepsius', ],
    license='BSD',
    zip_safe=True,
    install_requires=['regex', 'pygrok', 'pygtail'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Natural Language :: French',
    ],
)
