# WebLorean
A time-travel tool for web admins and IT security people.

## Introduction

The idea behind this tool is explained on the article "Abusing the Past",
originally published on 2600 Magazine, Volume 32, Issue One.  You can read
an online version here:
http://blogs.buanzo.com.ar/2015/05/abusing-the-past-a-2600-article-published-volume-32-number-one.html
The first release of WebLorean was in November, 2015:
http://blogs.buanzo.com.ar/2015/11/weblorean-the-abusing-the-past-script.html

For Ekoparty 2017, where WebLorean is set to be presented at Ekolabs, this
git release is made available.

## Installation

First, you need to clone the weblorean repository, or download it (github
provides the necessary options at https://github.com/buanzo/weblorean).

```
cd /usr/local/src
git clone https://github.com/buanzo/weblorean
```

WebLorean was developed and tested on Ubuntu Desktop 16.04 and 17.04.
All Python requirements can be installed using pip. Run the following
commands inside the project directory:

```
cd /usr/local/src/weblorean
pip install -r requirements.txt
playwright install
```

If you know what you are doing, you can install selenium and chromedriver
off PIP as well, but you might need to tweak WebLorean source and/or
specify special command line arguments. Selenium is, by itself, sometimes a
bit delicate.

## Usage

```
cd weblorean
./weblorean.py http://www.example.org
```
=======
### Available methods

WebLorean can gather historical IP addresses using several sources. Use
the `-m` option to select one of the following methods (default is `all`):

* `netcraft`
* `dnshistory`
* `dnstrails`
* `viewdns`

## What about Windows Subsystem for Linux?

If you are using Ubuntu under Windows 10 / WSL, you can run all non-SELENIUM
based methods. I dont think xvfb+pyvirtualdisplay are still WSL compatible,
although chromium DOES work. YMMV.
