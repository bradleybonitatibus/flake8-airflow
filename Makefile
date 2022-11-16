# Copyright 2022 Bradley Bonitatibus

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

.PHONY: test
test:
	tox -e py
	open ./htmlcov/index.html

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
	pip install -r requirements.txt

ci: clean deps test
