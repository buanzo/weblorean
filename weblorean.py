#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import socket
import argparse
import requests
import urllib3
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
from argparse import RawTextHelpFormatter
__author__ = "Arturo 'Buanzo' Busleiman"
__copyright__ = "Copyright (C) 2017 Arturo Alberto Busleiman"
__license__ = "GNU General Public License v3.0"
__version__ = "20170927"
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
            r = requests.get(url,
                             timeout=__default_timeout__,
                             verify=False)
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
        else:
            self.method = method
        target = target.lower()
        self.url = target
        self.fqdn = target.replace('http://', '').replace('https://', '')
        self.proto = self.url.split("://")[0]

        # ipv4_current holds all IPv4 addresses currently in DNS for fqdn
        self.ipv4_current = None  # updated by self.get_ipv4_records()

        # ipv4_history only holds past addresses, even if a current one
        # is listed historically:
        self.ipv4_history = None  # TODO:updated by self.get_hosting_history()

    def get_ipv4_records(self):  # TODO: support IPv6
        if self.proto is 'https':
            port = 443
        else:
            port = 80
        iplist = []
        try:
            infolist = socket.getaddrinfo(self.fqdn,
                                          port,
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

    def timetravelcheck(self):
        # This function crafts an http request for self.url, but connects
        # to historic ipv4 addresses for self.fqdn. This is the weblorean
        # concept, as explained on "Abusing the Past" (2600 Vol 32 Issue 1)
        curated_hh = self.ipv4_history
        for ip in self.ipv4_current:
            if ip in self.ipv4_history:
                curated_hh.remove(ip)
        if len(curated_hh) == 0:
            print("No historic IPs that are not current also. Nothing to do.")
            return
        print("Historic addresses, NO current ones: {}".format(curated_hh))
        for oldhost in curated_hh:
            # First, get html for oldhost's default website (no "Host:" header)
            url = '{}://{}/'.format(self.proto, oldhost)
            print("Getting html for default website at {}".format(url))
            try:
                r = requests.get(url,
                                 timeout=__default_timeout__,
                                 verify=False)
            except requests.Timeout:
                print("Timeout accessing {}".format(oldhost))
                continue
            except:
                print("Cant access default website. {} down?.".format(oldhost))
                continue
            if r.status_code is not requests.codes.ok:
                print("default website on {} is not 200 OK.".format(oldhost))
                continue
            default_html = r.text

            # Now, we get html for self.fqdn on oldhost
            headers = {'Host': self.fqdn}
            try:
                r = requests.get(url,
                                 headers=headers,
                                 timeout=__default_timeout__,
                                 verify=False)
            except requests.Timeout:
                print("Timeout accessing {} via {}".format(url, oldhost))
                continue
            except:
                print("Cannot access {} via {}.".format(url, oldhost))
                continue
            if r.status_code is not requests.codes.ok:
                print("Status for {} via {} is not 200.".format(url, oldhost))
                continue
            host_based_html = r.text

            # Now we also get a definitely non existent fqdn on oldhost
            headers = {'Host': self.fqdn[::-1]}  # reverse the fqdn string
            try:
                r = requests.get(url,
                                 headers=headers,
                                 timeout=__default_timeout__,
                                 verify=False)
            except requests.Timeout:
                print("Timeout trying inexistant host via {}".format(oldhost))
                continue
            except:
                print("Cannot access inexistant host via {}".format(oldhost))
            inexistant_host_based_html = r.text

            # So, let's see...
            if default_html == host_based_html:
                print("No luck")
                continue
            if host_based_html == inexistant_host_based_html:
                print("No luck")
                continue
            else:
                if r.status_code is requests.codes.ok:
                    print("{} seems accesible at {}".format(self.fqdn,
                                                            oldhost))
                else:
                    print("Not 200 OK, skipping.")
                continue

    def get_hosting_history(self):
        # TODO: call specific routines depending on self.method
        # those routines must return a []
        # finally, populate hosting_history whilst removing current
        # addresses.
        if self.method == 'netcraft':
            self.ipv4_history = self.netcraft()
            return(self.ipv4_history)
        elif self.method == 'manual':
            # TODO: read off an argument?
            return([])
        pass

    def netcraft(self, logpath='weblorean_chromedriver.log'):
        # TODO: add argparsing for these options, including chromedriver path
        display = Display(visible=0, size=(1360, 768))
        display.start()
        time.sleep(3)  # TODO: puaj
        service_args = ['--verbose']
        browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',
                                   service_args=service_args,
                                   service_log_path=logpath)
        time.sleep(3)  # TODO: puaj
#        browser.maximize_window()
        BASE = 'http://toolbar.netcraft.com/site_report?url'
        DATAURL = '{}={}'.format(BASE, self.url)
        try:
            print("SELENIUM: Accessing {}".format(DATAURL))
            ret = browser.get(DATAURL)
        except:
            print("SELENIUM: Exception. Exiting. Check {}".format(logpath))
            browser.quit()
            display.stop()
        try:
            HTML = browser.page_source
        except:
            print("SELENIUM: Exception reading html. Check {}".format(logpath))
            browser.quit()
            display.stop()

        HH = self.netcraft_scrape(html=HTML)
        browser.quit()
        display.stop()
        return(HH)

    def netcraft_scrape(self, html):
        # TODO: error checking
        soup = BeautifulSoup(html, "lxml")
        hs = soup.find('section',
                       class_='site_report_table',
                       id='history_table')
        try:
            trs = hs.find_all('tr')
        except:
            return([])
        iplist = []
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) == 0:
                continue
            iplist.append(tds[1].get_text())
        iplist = list(set(iplist))  # remove dupes
        return(iplist)

if __name__ == '__main__':
    print(_longprogname())
    # No concern for these warnings in this case:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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
            print("Current addresses: {}".format(wl.get_ipv4_records()))
            print("Historic addresses: {}".format(wl.get_hosting_history()))
            if len(wl.ipv4_history) == 0:
                print("No hosting history. Skipping target.")
                continue
            print(">>> Initiating Time Travel... <<<")
            wl.timetravelcheck()
