from __future__ import annotations

import pytest

import ibis


@pytest.fixture(scope="session")
def con():
    """Test fixture for Presto connection."""
    pytest.importorskip("prestodb")
    return ibis.presto.connect(
        host="localhost",
        port=8080,
        user="user",
        database="memory",
        schema="default",
    )


def test_basic_connection(con):
    """Test that we can connect to Presto."""
    assert con is not None
    assert con.name == "presto"


def test_version(con):
    """Test that we can get the Presto version."""
    version = con.version
    assert isinstance(version, str)
    assert len(version) > 0


def test_list_databases(con):
    """Test that we can list databases."""
    databases = con.list_databases()
    assert isinstance(databases, list)
    assert "default" in databases


def test_list_tables(con):
    """Test that we can list tables."""
    tables = con.list_tables()
    assert isinstance(tables, list)
