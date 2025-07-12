import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from weblorean import WebLorean


def test_viewdns_scrape():
    html = """
    <html><body><table>
        <tr><td>1.2.3.4</td><td>date</td></tr>
        <tr><td>5.6.7.8</td></tr>
    </table></body></html>
    """
    wl = WebLorean(target="http://example.com")
    ips = wl.viewdns_scrape(html)
    assert set(ips) == {"1.2.3.4", "5.6.7.8"}


def test_dnshistory_scrape():
    html = """
    <html><body>
        <a href='/dns-records/1.2.3.4.in-addr.arpa.html'>x</a>
        <a href='/dns-records/5.6.7.8.in-addr.arpa.html'>x</a>
    </body></html>
    """
    wl = WebLorean(target="http://example.com")
    ips = wl.dnshistory_scrape(html)
    assert set(ips) == {"1.2.3.4", "5.6.7.8"}


def test_dnstrails_scrape():
    html = """
    <html><body>
        <a href='/tools/lookup.htm?ip=8.8.8.8&date=2017-01-01'>x</a>
        <a href='/tools/lookup.htm?ip=9.9.9.9&date=2017-01-02'>x</a>
    </body></html>
    """
    wl = WebLorean(target="http://example.com")
    ips = wl.dnstrails_scrape(html)
    assert set(ips) == {"8.8.8.8", "9.9.9.9"}


def test_netcraft_scrape():
    html = """
    <html><body>
      <section class='site_report_table' id='history_table'>
        <tr><td>A</td><td>1.1.1.1</td></tr>
        <tr><td>A</td><td>2.2.2.2</td></tr>
      </section>
    </body></html>
    """
    wl = WebLorean(target="http://example.com")
    ips = wl.netcraft_scrape(html)
    assert set(ips) == {"1.1.1.1", "2.2.2.2"}
