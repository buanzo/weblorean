import os
import sys
import pytest
import argparse
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from weblorean import WLArgParseHelpers

class DummyResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def test_try_url_success(monkeypatch):
    def fake_get(url, timeout=None, verify=None):
        return DummyResponse(200)
    monkeypatch.setattr('requests.get', fake_get)
    assert WLArgParseHelpers.try_url('http://example.com') == 'http://example.com'


def test_try_url_non_200(monkeypatch):
    def fake_get(url, timeout=None, verify=None):
        return DummyResponse(404)
    monkeypatch.setattr('requests.get', fake_get)
    with pytest.raises(argparse.ArgumentTypeError):
        WLArgParseHelpers.try_url('http://example.com')


def test_try_url_timeout(monkeypatch):
    def fake_get(url, timeout=None, verify=None):
        raise requests.Timeout
    monkeypatch.setattr('requests.get', fake_get)
    with pytest.raises(argparse.ArgumentTypeError):
        WLArgParseHelpers.try_url('http://example.com')
