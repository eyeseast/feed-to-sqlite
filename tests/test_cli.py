import time
from pathlib import Path
from subprocess import Popen

import pytest
from click.testing import CliRunner
from feed_to_sqlite.cli import cli

TESTS = Path(__file__).parent


@pytest.fixture
def server():
    proc = Popen(["python", "-m", "http.server", "8000"])
    time.sleep(1)  # make sure server has started
    yield proc
    proc.kill()


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert 0 == result.exit_code
        assert result.output.startswith("cli, version ")


def test_with_server(server):
    runner = CliRunner()
    with runner.isolated_filesystem():
        url = "http://127.0.0.1:8000/tests/newsblur.xml"
        result = runner.invoke(cli, ["test.db", url])
        assert 0 == result.exit_code


def test_alter(server):
    runner = CliRunner()
    with runner.isolated_filesystem():
        newsblur = "http://127.0.0.1:8000/tests/newsblur.xml"
        instapaper = "http://127.0.0.1:8000/tests/instapaper.xml"
        result = runner.invoke(cli, ["--alter", "test.db", newsblur, instapaper])
        assert 0 == result.exit_code


def test_headers(server):
    runner = CliRunner()
    with runner.isolated_filesystem():
        url = "http://127.0.0.1:8000/tests/newsblur.xml"
        result = runner.invoke(cli, ["test.db", url, "-H", "user-agent", "test"])
        assert 0 == result.exit_code
