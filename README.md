[![Build Status](https://travis-ci.com/eyeseast/feed-to-sqlite.svg?branch=master)](https://travis-ci.com/eyeseast/feed-to-sqlite)

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

## Development

Tests use [pytest](https://docs.pytest.org/). Run `pytest tests/` to run the test suite.
