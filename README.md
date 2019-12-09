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

## Python API

TBD
