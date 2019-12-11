import pathlib

import feedparser
import pytest
import sqlite_utils

from feed_to_sqlite import ingest_feed


def feed(name):
    with open(pathlib.Path(__file__).parent / name) as f:
        return f.read()


@pytest.fixture
def newsblur():
    return feed("newsblur.xml")


@pytest.fixture
def instapaper():
    return feed("instapaper.xml")


@pytest.fixture
def db():
    return sqlite_utils.Database(memory=True)


def test_load_feed(db, newsblur):
    ingest_feed(db, feed_content=newsblur)

    assert "chrisamicos_blurblog" in db.table_names()

    table = db["chrisamicos_blurblog"]

    assert table.count == 25
