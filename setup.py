import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-paste_image",
    version="0.1",
    author="Justin Engel",
    author_email="jtengel08@gmail.com",
    description=("Django library for an image field that can be "
                 "set by copying and pasting an image into the browser."),
    license="MIT",
    keywords="django paste image",
    url="",
    packages=['paste_image'],
    package_data={'paste_image': ["templates/paste_image/widgets/*.html",
                                  "static/paste_image/*.js",
                                  "static/paste_image/*.html",
                                  "static/paste_image/*.css"]},
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 1.11",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
