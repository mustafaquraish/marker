import os
import shutil
import setuptools

os.makedirs('build/_scripts', exist_ok=True)
shutil.copyfile('marker/main.py', 'build/_scripts/marker')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='automark',
    version='1.0.5.1',
    scripts=['build/_scripts/marker'],
    author="Mustafa Quraish",
    license="MIT",
    author_email="mustafa@cs.toronto.edu",
    description="A highly configurable auto-marker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mustafaquraish/marker",
    packages=setuptools.find_packages(),
    py_modules=[
        'marker'
    ],
    install_requires=[
        'requests', 'pyyaml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
