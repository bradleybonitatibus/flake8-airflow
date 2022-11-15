.PHONY: test
test:
	tox -e py
	open ./htmlcov/index.html

.PHONY: lint
lint:
	tox -e linters

.PHONY: build
build: clean
	python setup.py sdist bdist_wheel

.PHONY: install
install:
	pip install .

.PHONY: clean
clean:
	rm -rf dist
	rm -rf build


.PHONY: deps
deps:
	pip install pip-tools
	pip-compile
	pip-compile -r dev-requirements.in
	pip install -r requirements.txt -r dev-requirements.txt
