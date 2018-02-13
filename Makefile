all: test lint

test:
	$(PYTHON) coverage run --source brambox setup.py test -q

lint:
	$(PYTHON) pycodestyle --max-line-length=200 ./brambox/ && \
	$(PYTHON) pycodestyle --max-line-length=200 ./scripts/ && \
	$(PYTHON) pycodestyle --max-line-length=200 ./tests/

coverage:
	$(PYTHON) coverage html --skip-covered && \
	$(PYTHON) coverage report

docs:
	cd ./docs && make clean html

.PHONY: test lint coverage docs
