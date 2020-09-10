from distutils.core import setup
setup(
  name = 'prebird',         # How you named your package folder (MyLib)
  packages = ['prebird'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='afl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Intended to help preprocessing birds songs',   # Give a short description about your library
  author = 'Liber Adrián Hernández Abad',                   # Type in your name
  author_email = 'liber.a.hernandez@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/RoyFocker',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/RoyFocker/preBird/archive/v0.1.0.tar.gz',    # I explain this later on
  keywords = ['bird', 'birds', 'audio','preprocessing','processing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'matplotlib',
          'scypi',
          'sklearn',
          'glob',
          'pickle',
          'statistics',
          'skimage',
          'playsound',
          'copy',
          'argparse'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)