from setuptools import setup

setup(name='brambox',
      version='0.0.1',
      description='Unified tools for generating PR curves, crunshing image data annotation sets and more',
      author='EAVISE',
      packages=['brambox',
                'brambox.annotations',
                'brambox.transforms'],
      scripts=['scripts/convert_annotations.py',
               'scripts/format_pascalvoc_to_darknet.py',
               'scripts/show_annotations.py',
               'scripts/swap_image_channel.py',
               'scripts/sparse_link.py',
               'scripts/replace_image_channel.py',
               'scripts/show_training_loss.py'],
      test_suite='tests', install_requires=['matplotlib', 'plotly'])
