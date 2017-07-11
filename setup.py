from setuptools import setup
try:
    import iou
except ImportError:
    iou = object()
    iou.__title__ = "py-iou"
    iou.__summary__ = "A python package to find optimal number of transactions betweeen friends"
    iou.__uri__ = "https://github.com/kdheepak/iou"

    iou.__author__ = "Dheepak Krishnamurthy"
    iou.__email__ = "kdheepak89@gmail.com"

    iou.__license__ = "Revised BSD License"
    iou.__copyright__ = "Copyright 2016 Dheepak Krishnamurthy"
    iou.__version__ = '1.1.1'

from os import path
from pip.req import parse_requirements

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    with open(path.join(here, 'README.md')) as f:
        long_description = f.read()

install_requires = [str(ir.req)
                    for ir in parse_requirements(
                        path.join(here, 'requirements.txt'),
                        session=False)]

setup(
    name=iou.__title__,
    version=iou.__version__,
    description=iou.__summary__,
    long_description=long_description,
    license=iou.__license__,
    url=iou.__uri__,
    author=iou.__author__,
    author_email=iou.__email__,
    packages=["iou", "iou.data"],
    entry_points={
        "console_scripts": [
            "iou = iou.run:main",
        ],
    },
    install_requires=install_requires,

    # dependency_links=[
    # "git+ssh://git@github.com/kdheepak89/click.git@7.0#egg=click-7.0"
    # ]
)
