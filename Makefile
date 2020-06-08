all: install

install:
	python3 setup.py bdist_wheel
	pip3 install dist/*

.PHONY: clean again

reinstall: clean
	python3 setup.py bdist_wheel
	pip3 install dist/*

uninstall:
	yes | pip3 uninstall marker

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist