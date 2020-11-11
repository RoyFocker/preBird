#!/usr/bin/python3
# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
  name = 'prebird',         
  packages = ['prebird'],   
  version = '1.3.0',      
  license='afl-3.0',      
  description = 'Intended to help preprocessing birds songs',   
  author = 'Liber Adrián Hernández Abad',                   
  author_email = 'liber.a.hernandez@gmail.com',      
  url = 'https://github.com/RoyFocker',   
  download_url = 'https://github.com/RoyFocker/preBird/archive/1.3.0.tar.gz',
  keywords = ['bird', 'birds', 'audio','preprocessing','processing'], 
  install_requires=[
          'numpy',
          'matplotlib',
          'scipy',
          'sklearn',
          'glob3',
          'scikit-image',
          'playsound'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)