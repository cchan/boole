#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='boole',
    version='0.0.1',
    description='A software to verify textual formulae and proofs as used in SE 212 at the University of Waterloo.',
    url='https://github.com/cchan/boole',
    keywords='logic education',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Education :: Computer Aided Instruction (CAI)',
        'Topic :: Education :: Testing',
    ],
    zip_safe=False,
)
