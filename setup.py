import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='automark',
    version='1.0.0',
    scripts=['automark', 'prepare', 'lms-download',
             'lms-upload-marks', 'lms-upload-reports',
             'lms-set-status'],
    author="Mustafa Quraish",
    author_email="mustafa@cs.toronto.edu",
    description="A highly configurable auto-marker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mustafaquraish/marker",
    packages=setuptools.find_packages(),
    py_modules=[
        'testcases', 'utils', 'marksheet', 'config',
        'lms'
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
