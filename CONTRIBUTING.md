# Coding guidelines
## Coding style

This project follows the [pep8](https://www.python.org/dev/peps/pep-0008/) coding style guide
(except for the ridiculous max 79 character line length).

You can validate your contributed code on style guide violations using the following tool:

```
pip install pep8
```

NOTE: This project is python 3 so on some systems you might want to use 'pip3' instead of 'pip'

Run it on the repo with:

```
cd brambox
pep8 --max-line-length=200 .
```

## Adding a package

A package in python is a folder containing one or more python modules (.py files) and a '__init__.py' file where the name
of the folder is the name of the package.

If you add a new package, mension its name in the 'setup.py' build script by adding an entry in the 'packages' list.

## Adding a script

Scripts from the script folder that accept command line options must use python's 'argparse' library to parse the
commandline options. See the scripts folder for examples.

If you add a scrip, mension its name in the 'setup.py' build script by adding an entry in the 'scripts' list.