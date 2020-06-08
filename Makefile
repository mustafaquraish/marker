all: build

build:
	python3 setup.py bdist_wheel

install: build
	pip3 install dist/*

reinstall: clean uninstall install

uninstall:
	yes | pip3 uninstall marker

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist