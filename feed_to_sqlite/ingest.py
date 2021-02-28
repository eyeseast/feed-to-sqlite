import datetime
import feedparser
import httpx
from slugify import Slugify
from sqlite_utils import Database

slugify = Slugify(to_lower=True, separator="_", max_length=100)

FEEDS_TABLE = "feeds"


def ingest_feed(
    db, *, url=None, feed_content="", table_name=None, normalize=None, client=None
):
    """
    `db` is a path or Database instance

    if `table_name` is None, auto create from feed title

    if `url` is given, fetch and parse

    if `feed_content` is given, but not url, parse that

    `normalize` is a function that will be called on each feed item, useful for fixing links
    or doing additional work. It's signature is normalize(table, entry, feed_details).

    `client` is an instance of `httpx.Client` to pool requests.
    """
    if not isinstance(db, Database):
        db = Database(db)

    if client is None:
        client = httpx.Client()

    if url:
        r = client.get(url)
        r.raise_for_status()
        feed_content = r.text

    f = feedparser.parse(feed_content)
    if not f.entries:
        # todo raise something here
        return

    feeds = get_feeds_table(db, FEEDS_TABLE)
    feeds.upsert(extract_feed_fields(feeds, f.feed), pk="id")

    entries = get_entries_table(db, table_name, f.feed)

    if not callable(normalize):
        normalize = extract_entry_fields

    rows = (normalize(entries, entry, f.feed, client) for entry in f.entries)
    rows = filter(bool, rows)

    entries.upsert_all(rows, pk="id")


def get_entries_table(db, table_name, feed):
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
        foreign_keys=[("feed", "feeds")],
    )


def get_feeds_table(db, table_name=FEEDS_TABLE):
    """
    Create our default feeds table
    """
    table = db[table_name]

    if not table.exists():
        table.create(
            {
                "id": str,
                "title": str,
                "subtitle": str,
                "link": str,
                "author": str,
                "updated": datetime.datetime,
            },
            pk="id",
        )

    return table


def extract_entry_fields(table, entry, feed, client=None):
    """
    Given a table intance, entry dict and feed details, extract fields found in the table
    """
    row = {"feed": feed.get("id", feed.link)}
    for key in table.columns_dict:
        value = entry.get(key)
        if value is not None:
            row[key] = value

    return row


def extract_feed_fields(table, feed):
    """
    Similar to extract_entry_fields, but for top-level metadata
    """
    row = {}
    for key in table.columns_dict:
        value = feed.get(key)
        if value is not None:
            row[key] = value

    # is there ever a case where a feed doesn't have a link?
    row.setdefault("id", row["link"])
    row.setdefault("updated", datetime.datetime.now())

    return row
