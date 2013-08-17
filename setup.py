__author__ = 'romus'

from setuptools import setup, find_packages
from os.path import join, dirname
import statistic4text

setup(
    name='statistic4text',
    version=statistic4text.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    description="Gathering statistics on the text "
                "Python packages",
    author="romus",
    author_email="vkromus@gmail.com",
    license="GPL v3", requires=['pymongo', 'chardet'],
)