from setuptools import setup

setup(
    name='mandelbrot',
    version='0.1',
    author='Juan Schandin',
    author_email='juan.schandin@avature.net',
    py_modules=['mandelbrot'],
    install_requires=[
        'Pygame',
        'Pytoml',
    ],
    entry_points="""
    [console_scripts]
    mandelbrot = mandelbrot:cli
    """
)
