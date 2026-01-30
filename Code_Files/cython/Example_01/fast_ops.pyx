# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 08:24:54 2026

@author: kec994


This expects a NumPy float32 2D array.

It runs fast because the nested loops are compiled to C.
"""


# fast_ops.pyx
# cython: language_level=3

import numpy as np
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def clamp_inplace(cnp.ndarray[cnp.float32_t, ndim=2] img, float lo, float hi):
    """
    Clamp a 2D float32 NumPy array in-place: img = min(max(img, lo), hi)
    """
    cdef Py_ssize_t i, j
    cdef Py_ssize_t H = img.shape[0]
    cdef Py_ssize_t W = img.shape[1]
    cdef float v

    for i in range(H):
        for j in range(W):
            v = img[i, j]
            if v < lo:
                img[i, j] = lo
            elif v > hi:
                img[i, j] = hi

    return img  # returning is optional since it's in-place


@cython.boundscheck(False)
@cython.wraparound(False)
def normalize_inplace(cnp.ndarray[cnp.float32_t, ndim=2] img, float mean, float std):
    """
    Normalize in-place: (img - mean) / std
    """
    cdef Py_ssize_t i, j
    cdef Py_ssize_t H = img.shape[0]
    cdef Py_ssize_t W = img.shape[1]
    cdef float invstd

    if std == 0.0:
        raise ValueError("std must be non-zero")

    invstd = 1.0 / std

    for i in range(H):
        for j in range(W):
            img[i, j] = (img[i, j] - mean) * invstd

    return img
