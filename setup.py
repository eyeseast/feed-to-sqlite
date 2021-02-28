from setuptools import setup
import os

VERSION = "0.5.0"

README = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")


def get_long_description():
    with open(README, encoding="utf-8") as f:
        return f.read()


setup(
    name="feed-to-sqlite",
    version=VERSION,
    description="Save an RSS or ATOM feed to a SQLITE database",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Chris Amico",
    license="Apache License, Version 2.0",
    packages=["feed_to_sqlite"],
    entry_points="""
        [console_scripts]
        feed-to-sqlite=feed_to_sqlite.cli:cli
    """,
    install_requires=[
        "sqlite-utils>=2.22",
        "httpx",
        "feedparser",
        "awesome-slugify",
    ],
    extras_require={"test": ["pytest"]},
    tests_require=["feed-to-sqlite[test]"],
    url="https://github.com/eyeseast/feed-to-sqlite",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Database",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
