from distutils.core import setup

setup(name='brambox',
      version='0.1',
      description='Unified tools for generating PR curves, crunshing image data annotation sets and more',
      author='EAVISE',
      packages=['brambox', 'brambox.annotations'],
      scripts=['scripts/format_vatic_to_dollar.py']
     )
