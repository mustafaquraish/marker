import os
import shutil
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='marker',
    version='2.1.3',
    entry_points={
    'console_scripts': [
            'marker = marker.repl.repl:main',
        ],
    },
    author="Mustafa Quraish",
    license="MIT",
    author_email="mustafa@cs.toronto.edu",
    description="A highly configurable auto-marker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mustafaquraish/marker",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests', 'pyyaml', 'aiohttp', 'aiofiles', 'cmd2', 'rich', 'jinja2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
