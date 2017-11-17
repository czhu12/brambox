import setuptools as setup

def find_packages():
    return ['brambox'] + ['brambox.'+p for p in setup.find_packages('brambox')]

def find_scripts():
    return setup.findall('scripts')

setup.setup(name='brambox',
            version='1.0.0',
            author='EAVISE',
            description='Unified tools for generating PR curves, crunshing image data annotation sets and more',
            long_description=open('README.md').read(),
            packages=find_packages(),
            scripts=find_scripts(),
            test_suite='tests')
