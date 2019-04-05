#!/usr/bin/env python
import os

from setuptools import find_packages, setup

# https://packaging.python.org/guides/single-sourcing-package-version/
version = {}
with open(os.path.join("src", "intergalactic", "__init__.py")) as version_file:
    exec(version_file.read(), version)


with open("README.rst") as readme_file:
    long_description = readme_file.read()

# https://packaging.python.org/guides/distributing-packages-using-setuptools
# http://blog.ionelmc.ro/2014/05/25/python-packaging/
setup(
    name="intergalactic",
    version=version["__version__"],
    description="Galactic elements Q-Matrix generator",
    author="Juanjo Bazán",
    author_email="hello@juanjobazan.com",
    url="https://github.com/xuanxu/intergalactic",
    download_url="https://github.com/xuanxu/intergalactic",
    license="MIT",
    keywords=[
        "galaxies",
        "models",
        "astrophysics",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyyaml>=3.13",
        "numpy>=1.16",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["sample_input/*"]},
    entry_points={"console_scripts": ["intergalactic = intergalactic.cli:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    long_description=long_description,
    include_package_data=True,
    zip_safe=False,
)
