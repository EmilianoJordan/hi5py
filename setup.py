#! /usr/bin/env python3
"""The presence of this file ensures the support
of pip editable mode *with setuptools only*.

Thanks to work done by Sorin Sbarnea on cookiecutter
https://github.com/cookiecutter/cookiecutter/pull/1577
"""
import setuptools

setuptools.setup(
    use_scm_version=True,
    setup_requires=["setuptools_scm[toml]>=3.5.0"],
)
