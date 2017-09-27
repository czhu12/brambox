from distutils.core import setup

setup(name='brambox',
      version='0.0.1',
      description='Unified tools for generating PR curves, crunshing image data annotation sets and more',
      author='EAVISE',
      packages=['brambox', 'brambox.annotations', 'brambox.transforms'],
      scripts=['scripts/format_vatic_to_dollar.py', 'scripts/show_annotations.py', 'scripts/swap_image_channel.py'])
