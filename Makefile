all: test lint

test:
	coverage run --source brambox setup.py test -q

lint:
	pycodestyle --max-line-length=200 ./brambox/ && \
	pycodestyle --max-line-length=200 ./scripts/ && \
	pycodestyle --max-line-length=200 ./tests/

coverage:
	coverage html --skip-covered && \
	coverage report

docs:
	cd ./docs && make clean html

.PHONY: test lint coverage docs
