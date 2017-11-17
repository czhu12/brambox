# Coding guidelines
## Coding style

This project follows the [pep8](https://www.python.org/dev/peps/pep-0008/) coding style guide
(except for the ridiculous max 79 character line length).

You can validate your contributed code on style guide violations using the following tool:

```
pip install pep8
```

NOTE: This project is python 3.6 so on some systems you might want to use 'pip3.6' or 'python3.6 -m pip' instead of 'pip'

Run it on the repo with:

```
cd brambox
pep8 --max-line-length=200 .
```

## Running scripts when developping

If you already installed brambox on your system in the past and you are developing on brambox, you might what to use
brambox from your git clone instead of the one installed on your system. To do that, just make sure you execute a script
using brambox from inside the root folder of the git repo. Python will look for packages in the current directory first
before trying to find them in your python path. For example:

```
cd brambox_git_clone
./scripts/script_to_test.py     # will use brambox from the git repo
```

## Adding a package

A package in python is a folder containing one or more python modules (.py files) and a '\_\_init\_\_.py' file where the name
of the folder is the name of the package.

If you add a new package, mension its name in the 'setup.py' build script by adding an entry in the 'packages' list.

## Adding a script

Scripts from the script folder that accept command line options must use python's 'argparse' library to parse the
commandline options. See the scripts folder for examples.

If you add a scrip, mension its name in the 'setup.py' build script by adding an entry in the 'scripts' list.

## Creating unit tests

If you want to add a unit test module, create a file in 'tests' starting with the 'test\_' prefix.
We are using python's 'unittest' package so see python's unittest help or an existing test suite in brambox for examples.

## Running unit tests

The 'tests' folder contains unit test modules for the brambox packages. You can run all tests with:

```
python setup.py test
```

If you want to run only one unit test module during test development:

```
python test/test_my_module_under_test.py
```

