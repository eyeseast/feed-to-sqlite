import datetime
import feedparser
import requests
from slugify import Slugify
from sqlite_utils import Database

slugify = Slugify(to_lower=True, separator="_", max_length=100)


def ingest_feed(db, *, url=None, feed_content="", table_name=None, normalize=None):
    """
    `db` is a path or Database instance
    
    if `table_name` is None, auto create from feed title
    
    if `url` is given, fetch and parse
    
    if `feed_content` is given, but not url, parse that

    `normalize` is a function that will be called on each feed item, useful for fixing links
    or doing additional work. It's signature is normalize(table, entry, feed_details).
    """
    if not isinstance(db, Database):
        db = Database(db)

    if url:
        r = requests.get(url)
        r.raise_for_status()
        feed_content = r.text

    f = feedparser.parse(feed_content)
    if not f.entries:
        # todo raise something here
        return

    table = get_table(db, table_name, f.feed)

    if not callable(normalize):
        normalize = extract_fields

    rows = (normalize(table, entry, f.feed) for entry in f.entries)

    table.upsert_all(rows, pk="id")


def get_table(db, table_name, feed):
    "Get or create a table"
    if not table_name:
        table_name = slugify(feed.title)

    # this is a good hook to create a custom table
    # and then use normalize to reshape data accordingly
    if table_name in db.table_names():
        return db[table_name]

    # default table layout
    return db[table_name].create(
        {
            "id": str,
            "feed": str,
            "title": str,
            "description": str,
            "published": datetime.datetime,
            "updated": datetime.datetime,
            "link": str,
        },
        pk="id",
    )


def extract_fields(table, entry, feed):
    """
    Given a table intance, entry dict and feed details, extract fields found in the table
    """
    row = {"feed": feed.title}
    for key in table.columns_dict:
        value = entry.get(key)
        if value is not None:
            row[key] = value

    return row
