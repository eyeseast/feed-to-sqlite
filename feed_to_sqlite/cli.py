#!/usr/bin/env python
import click
import httpx

from .ingest import ingest_feed


@click.command()
@click.option("--table", help="Table name for all items")
@click.argument(
    "database",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("urls", nargs=-1)
def cli(database, urls, table=None):
    with httpx.Client() as client:
        for url in urls:
            ingest_feed(database, table_name=table, url=url, client=client)
