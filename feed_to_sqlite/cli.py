#!/usr/bin/env python
import click
import httpx

from .ingest import ingest_feed


@click.command()
@click.version_option()
@click.option("--table", help="Table name for all items")
@click.option(
    "--alter", is_flag=True, default=False, help="Add missing fields to table"
)
@click.argument(
    "database",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("urls", nargs=-1)
def cli(database, urls, table=None, alter=False):
    with httpx.Client() as client:
        for url in urls:
            ingest_feed(database, table_name=table, url=url, client=client, alter=alter)
