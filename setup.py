from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'queens',
    ext_modules = cythonize("queens.pyx")
)
