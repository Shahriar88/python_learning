# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 08:26:53 2026

@author: kec994
"""
# After building: import fast_ops


# sudo apt update
# sudo apt install -y python3-dev build-essential
# python3 -m pip install cython numpy setuptools

# OR
# conda install cython numpy setuptools
# pip install cython numpy setuptools

# python build_cython.py build_ext --inplace



# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np


f_name = 'fast_ops'
ext = Extension(
    name=f_name,
    sources=[f"{f_name}.pyx"],
    include_dirs=[np.get_include()],
)

setup(
    name=f_name,
    ext_modules=cythonize(
        [ext],
        compiler_directives={"language_level": "3"},
    ),
)
