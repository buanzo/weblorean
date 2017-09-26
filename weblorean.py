#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import socket
import argparse
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from argparse import RawTextHelpFormatter

__author__ = "Arturo 'Buanzo' Busleiman"
__copyright__ = "Copyright (C) 2017 Arturo Alberto Busleiman"
__license__ = "GNU General Public License v3.0"
__version__ = "20170924"
__longprogname__ = ">>> Weblorean <<<"

__default_timeout__ = 30


def _disclaimer():
    msg = """
This program is provided as is.
No warranties, etc, etc. Standard open source disclaimer.
License: {}
""".format(__license__)
    return(msg)


def _longprogname():
    msg = "{} Version: {}\nBy {}".format(__longprogname__,
                                         __version__,
                                         __author__)
    return(msg)


class WLArgParseHelpers():
    @classmethod
    def try_url(cls, url):
        errmsg = "{} inaccesible or invalid (http://?)".format(url)
        timeout_errmsg = "Timeout trying to access {}".format(url)
        try:
            r = requests.get(url, timeout=__default_timeout__)
        except requests.Timeout:
            raise argparse.ArgumentTypeError(timeout_errmsg)
        except:
            raise argparse.ArgumentTypeError(errmsg)
        if r.status_code is not requests.codes.ok:
            raise argparse.ArgumentTypeError(errmsg)
        return(url)


class WebLorean():
    # First method is always the default one
    METHODS = ('netcraft', 'manual',)

    def __init__(self, target=None, method=None):
        # Target http validation implemented on ArgParser via type=
        if target is None:
            return(None)
        if method is None:
            self.method = WebLorean.METHODS[0]
        target = target.lower()
        self.url = target
        self.fqdn = target.replace('http://', '').replace('https://', '')

        # ipv4_current lists all IPv4 addresses currently in DNS for fqdn
        self.ipv4_current = None  # updated by self.get_ipv4_records()

        # ipv4_history only holds past addresses, even if a current one
        # is listed historically:
        self.ipv4_history = None  # TODO:updated by self.get_hosting_history()

        # raise ValueError("dsadsa")  #TODO: actually use

    def get_ipv4_records(self):  # TODO: support IPv6
        iplist = []
        try:
            infolist = socket.getaddrinfo(self.fqdn,
                                          80,
                                          socket.AF_INET,
                                          socket.SOCK_STREAM)
        except:
            pass
        else:
            for x in infolist:
                iplist.append(x[4][0])
        finally:
            self.ipv4_current = iplist
            return(iplist)

    def get_hosting_history(self):
        # TODO: call specific routines depending on self.method
        # those routines must return a []
        # finally, populate hosting_history whilst removing current
        # addresses.
        if self.method == 'netcraft':
            return(self.netcraft())
        elif self.method == 'manual':
            # TODO: read off an argument?
            return([])
        pass

    def netcraft(self):
        display = Display(visible=0, size=(1360, 768))
        display.start()
        service_log_path = 'weblorean_chromedriver.log'
        service_args = ['--verbose']
        browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',
                                   service_args=service_args,
                                   service_log_path=service_log_path)

    def netcraft_scrape(self, html):
        # TODO: error checking
        soup = BeautifulSoup(html)
        hs = soup.find('section',
                       class_='site_report_table',
                       id='history_table')
        trs = hs.find_all('tr')
        iplist = []
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) == 0:
                continue
            iplist.append(tds[1].get_text())
        iplist = list(set(iplist))  # remove dupes
        return(iplist)

    def finalize(self):
        # TODO: webdriver quit() and cleanup
        print("WebLorean()::finalize()")

if __name__ == '__main__':
    print(_longprogname())
    parser = argparse.ArgumentParser(description=_disclaimer(),
                                     formatter_class=RawTextHelpFormatter)
    # TODO: add other methods and apply argparse validations
    methods = WebLorean.METHODS
    help = "Method to obtain hosting history (Default: {})".format(methods[0])
    parser.add_argument("-m", "--method",
                        default=methods[0],
                        help=help,
                        choices=WebLorean.METHODS)
    parser.add_argument("--version",
                        help="Show version",
                        action='version',
                        version=_disclaimer())
    parser.add_argument("targets",
                        help="website[s] to check [*WITH* http/https://]",
                        nargs='+',
                        type=WLArgParseHelpers.try_url)
    args = parser.parse_args()
    for target in args.targets:
        # Initialize an instance of the WebLorean class
        # which will run basic checks on target and raise
        # an exception on error
        print("\nStarting WebLorean for {}".format(target))
        try:
            wl = WebLorean(target=target,
                           method=args.method)
        except ValueError as err:
            print("Err >> WebLorean: Exception: {}".format(target, err))
            continue
        except:
            print("Err >> Unexpected WebLorean error:", sys.exc_info()[0])
        else:
            print("This gets executed when no exceptions happen")
            pprint(wl.get_ipv4_records())
            wl.finalize()
