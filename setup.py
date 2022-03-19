#!/usr/bin/env python
from setuptools import find_packages, setup  # type: ignore

extras_require = {
    "test": [  # `test` GitHub Action jobs uses this
        "pytest-xdist",  # multi-process runner
        "pytest-cov",  # Coverage analyzer plugin
        "pytest-mock",  # For creating mocks
    ],
    "lint": [
        "black>=21.12b0,<22.0",  # auto-formatter and linter
        "mypy>=0.941,<1.0",  # Static type analyzer
        "types-PyYAML",  # NOTE: Needed due to mypy typeshed
        "types-requests",  # NOTE: Needed due to mypy typeshed
        "flake8>=3.9.2,<4.0",  # Style linter
        "flake8-breakpoint>=1.1.0,<2.0.0",  # detect breakpoints left in code
        "flake8-print>=4.0.0,<5.0.0",  # detect print statements left in code
        "isort>=5.10.1,<6.0",  # Import sorting linter
    ],
    "release": [  # `release` GitHub Action job uses this
        "setuptools",  # Installation tool
        "wheel",  # Packaging tool
        "twine",  # Package upload tool
    ],
}

# NOTE: `pip install -e .[dev]` to install package
extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["release"]
)

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="pypi_debugger",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Debug dependency issues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juliya Smith",
    author_email="juliya@juliyasmith.com",
    url="https://github.com/unparalleled-js/pypi-debugger",
    include_package_data=True,
    install_requires=[
        "click>=8.0.1,<9.0",
        "python-dateutil>=2.8.2,<3.0",
        "pipdeptree>=2.2.1,<3.0",
        "pypistats>=1.0,<2.0",
        "requests>=2.27.1,<3.0"
    ],
    entry_points={
        "console_scripts": ["pypid=pypi_debugger.cli:cli"],
    },
    python_requires=">=3.10.1,<3.11",
    extras_require=extras_require,
    py_modules=["pypi_debugger"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="pypi",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"pypi_debugger": ["py.typed"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.10",
    ],
)
