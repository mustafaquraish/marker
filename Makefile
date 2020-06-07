
all:
	python3 setup.py bdist_wheel
	pip3 install dist/*

.PHONY: clean again

again: clean
	python3 setup.py bdist_wheel
	pip3 install dist/*

clean:
	yes | pip3 uninstall automark