# -*- coding: utf-8 -*-
"""Unit tests for tweens.py"""
import mock
import pytest
from pyramid.httpexceptions import HTTPClientError
from pyramid.httpexceptions import HTTPInternalServerError
from pyramid.response import Response

from pyramid_swagger.load_schema import SchemaAndResolver
from pyramid_swagger.tween import schema_and_resolver_for_request
from pyramid_swagger.tween import prepare_body


def test_swagger_schema_for_request_different_methods():
    """Tests that schema_and_resolver_for_request() checks the request
    method."""
    mock_request = mock.Mock(
        path="/foo/bar",
        method="GET"
    )
    mock_schema_map = mock.Mock(items=mock.Mock(return_value=[
        (('/foo/{bars}', 'PUT'), 1234),
        (('/foo/{bars}', 'GET'), 666)
    ]))
    sar = SchemaAndResolver(
        schema_map=mock_schema_map,
        resolver=mock.ANY,
    )
    value, _ = schema_and_resolver_for_request(mock_request, [sar])
    assert value == 666


def test_swagger_schema_for_request_not_found():
    """Tests that schema_and_resolver_for_request() raises exceptions when
    a path is not found.
    """
    mock_request = mock.Mock(
        path="/foo/bar",
        method="GET"
    )
    mock_schema_map = mock.Mock(items=mock.Mock(return_value=[]))
    sar = SchemaAndResolver(
        schema_map=mock_schema_map,
        resolver=mock.ANY,
    )
    with pytest.raises(HTTPClientError) as excinfo:
        schema_and_resolver_for_request(mock_request, [sar])
    assert '/foo/bar' in str(excinfo)
    assert 'Could not find ' in str(excinfo)


def test_response_charset_missing_raises_5xx():
    with pytest.raises(HTTPInternalServerError):
        prepare_body(
            Response(content_type='foo')
        )
