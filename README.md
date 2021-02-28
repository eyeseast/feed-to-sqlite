[![Build Status](https://travis-ci.com/eyeseast/feed-to-sqlite.svg?branch=master)](https://travis-ci.com/eyeseast/feed-to-sqlite)
[![Tests](https://github.com/eyeseast/feed-to-sqlite/workflows/Test/badge.svg)](https://github.com/eyeseast/feed-to-sqlite/actions?query=workflow%3ATest)
[![PyPI](https://img.shields.io/pypi/v/feed-to-sqlite.svg)](https://pypi.org/project/feed-to-sqlite/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/eyeseast/feed-to-sqlite/blob/master/LICENSE)

# feed-to-sqlite

Download an RSS or Atom feed and save it to a SQLite database. This is meant to work well with [datasette](https://github.com/simonw/datasette).

## Installation

```sh
pip install feed-to-sqlite
```

## CLI Usage

Let's grab the ATOM feeds for [items I've shared on NewsBlur](http://chrisamico.newsblur.com/social/rss/35501/chrisamico) and [my instapaper favorites](https://www.instapaper.com/starred/rss/13475/qUh7yaOUGOSQeANThMyxXdYnho) save each its own table.

```sh
feed-to-sqlite feeds.db http://chrisamico.newsblur.com/social/rss/35501/chrisamico https://www.instapaper.com/starred/rss/13475/qUh7yaOUGOSQeANThMyxXdYnho
```

This will use a SQLite database called `feeds.db`, creating it if necessary. By default, each feed gets its own table, named based on a slugified version of the feed's title.

To load all items from multiple feeds into a common (or pre-existing) table, pass a `--table` argument:

```sh
feed-to-sqlite feeds.db --table links <url> <url>
```

That will put all items in a table called `links`.

Each feed also creates an entry in a `feeds` table containing top-level metadata for each feed. Each item will have a foreign key to the originating feed. This is especially useful if combining feeds into a shared table.

## Python API

One function, `ingest_feed`, does most of the work here. The following will create a database called `feeds.db` and download my NewsBlur shared items into a new table called `links`.

```python
from feed_to_sqlite import ingest_feed

url = "http://chrisamico.newsblur.com/social/rss/35501/chrisamico"

ingest_feed("feeds.db", url=url, table_name="links")
```

### Transforming data on ingest

When working in Python directly, it's possible to pass in a function to transform rows before they're saved to the database.

The `normalize` argument to `ingest_feed` is a function that will be called on each feed item, useful for fixing links or doing additional work.

It's signature is `normalize(table, entry, feed_details, client)`:

- `table` is a SQLite table ([from sqlite-utils](https://sqlite-utils.datasette.io/en/stable/python-api.html#accessing-tables))
- `entry` is one feed item, as a dictionary
- `feed_details` is a dictionary of top-level feed information, as a dictionary
- `client` is an instance of `httpx.Client`, which can be used for outgoing HTTP requests during normalization

That function should return a dictionary representing the row to be saved. Returning a falsey value for a given row will cause that row to be skipped.

## Development

Tests use [pytest](https://docs.pytest.org/). Run `pytest tests/` to run the test suite.
