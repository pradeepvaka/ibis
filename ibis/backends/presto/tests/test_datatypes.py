from __future__ import annotations

import pytest

import ibis.expr.datatypes as dt
from ibis.backends.presto import Backend


def test_type_mapper():
    """Test that the PrestoType mapper works correctly."""
    backend = Backend()
    type_mapper = backend.compiler.type_mapper

    # Test basic types
    assert type_mapper.from_string("integer") == dt.Int32(nullable=True)
    assert type_mapper.from_string("bigint") == dt.Int64(nullable=True)
    assert type_mapper.from_string("double") == dt.Float64(nullable=True)
    assert type_mapper.from_string("varchar") == dt.String(nullable=True)
    assert type_mapper.from_string("boolean") == dt.Boolean(nullable=True)


@pytest.mark.parametrize(
    "ibis_type,expected_sql_type",
    [
        (dt.int32, "INT"),
        (dt.int64, "BIGINT"),
        (dt.float64, "DOUBLE"),
        (dt.string, "VARCHAR"),
        (dt.boolean, "BOOLEAN"),
    ],
)
def test_ibis_to_sql_type(ibis_type, expected_sql_type):
    """Test that Ibis types are correctly converted to Presto SQL types."""
    backend = Backend()
    type_mapper = backend.compiler.type_mapper
    sql_type = type_mapper.from_ibis(ibis_type)
    assert expected_sql_type in sql_type.sql("presto")
