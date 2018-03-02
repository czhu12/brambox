Coding guidelines
=================
Here are some conventions we use when coding for brambox.  
For some actual guides on how to write custom parts for brambox,
take a look [here](https://eavise.gitlab.io/brambox/notes/02-extending.html).


## Development for brambox
If you already installed brambox on your system in the past and you are developing on brambox,
you might want to use brambox from your git clone instead of the one installed on your system.
The easiest way to accomplish this is to set up a custom python virtual environment for brambox
and install brambox as development.
```bash
# Activate new virtual environment
workon brambox_env
cd brambox_git_clone

# Install brambox
pip install -r develop.txt
```
> This project is python 3.6 so be sure to select the right version of python when creating your virtual environment.

### Coding style
This project follows the [pep8](https://www.python.org/dev/peps/pep-0008/) coding style guide
(except for the ridiculous max 79 character line length).  
You can validate your contributed code on style guide violations by running `make lint` in the root directory of the repo.

### Unit tests
The _tests_ folder contains unit test modules for the brambox packages. You can run all tests with `make test`.   
If you want to run only one unit test module during test development, use the following command:
```bash
python test/test_my_module.py
```

### Documentation
The documentation of the latest release of brambox can always be found [here](eavise.gitlab.io/brambox).  
If you want to check out the documentation of an earlier release or if you want to use the development version,
you will need to build it yourself with `make docs`.
The documentation will then be available in _docs/.build/html/index.html_.  
This project uses [Sphinx 1.7](https://github.com/sphinx-doc/sphinx) with napoleon to generate the documentation.
The documentation consists of docstrings in the source code using the [google style](http://www.sphinx-doc.org/en/stable/ext/napoleon.html#google-vs-numpy).


## Submitting to brambox
If you added some new things to brambox and want to share it with everyone, feel free to send in a pull request.
To ease the process of accepting your PR, here are some key points that need to be completed.

- [ ] The added functionality is not too specific for your use case. If you are not sure whether this is the case, open an issue before starting to code.
- [ ] A unit test covers your functionality and proves it works correctly.
- [ ] All unit tests pass and linting is ok. Check this by running `make`.
- [ ] All _exposed_ functions, classes and methods have been documented with google style docstrings and clearly explain the functionality. The documentation is added to the correct _.rst_ file.
- [ ] If a script is added, it uses _argparse_ and the usage is documented when using the `--help` functionality.


## Core developers
This is only intended for core developers, but can be used by everyone.  
Since we do not want any code that fails the linting or unit tests in the `master` or `develop` branches
(or any other branches really, but certainly not those),
we count on it that core developers check the code before pushing to these branches.
Of course all developers are still human and might actually forget this!  
This is why the CI of this gitlab repo checks the linting and unit tests of every branch,
whenever someone pushes to it. If it fails, the culprit will be send an annoying email to urge him to fix it asap!

Because we got tired of getting this __F$!#__ emails,
we decided to use some git-hooks to never accidentally push wrong code to the repository.
Here is the code of these hooks, so that everyone can use it if they want to.
(Make sure to use the exact paths for the files, otherwise it will not work)

_.git/hooks/pre-commit_
```bash
#!/usr/bin/env bash
#
# Check linting before commit
#

# Set right python env
source /usr/local/bin/virtualenvwrapper.sh &>/dev/null
workon bb &>/dev/null

# Check linting
make lint &>/dev/null
status=$?
if [ "$status" -ne 0 ]; then
    echo "Linting failed" >&2
    exit 2
fi

# Everything OK
exit 0
```

_.git/hooks/pre-push_
```bash
#!/usr/bin/env bash
#
# Check linting and unit tests before pushing to remote
# Check for WIP tags in commit messages
#

# Set right python env
source /usr/local/bin/virtualenvwrapper.sh &>/dev/null
workon py36 &>/dev/null

# Check unit tests
make test &>/dev/null
status=$?
if [ "$status" -ne 0 ]; then
    echo "Unit tests failed" >&2
    exit 1
fi

# Check linting
make lint &>/dev/null
status=$?
if [ "$status" -ne 0 ]; then
    echo "Linting failed" >&2
    exit 2
fi

# Check for WIP in commit messages
z40=0000000000000000000000000000000000000000
while read local_ref local_sha remote_ref remote_sha
do
	if [ "$local_sha" = $z40 ]
	then
		# Handle delete
		:
	else
		if [ "$remote_sha" = $z40 ]
		then
			# New branch, examine all commits
			range="$local_sha"
		else
			# Update to existing branch, examine new commits
			range="$remote_sha..$local_sha"
		fi

		# Check for WIP commit
		commit=`git rev-list -n 1 --grep '^WIP' "$range"`
		if [ -n "$commit" ]
		then
			echo >&2 "Found WIP commit in $local_ref, not pushing"
			exit 3
		fi
	fi
done

# Everything OK
exit 0

```
