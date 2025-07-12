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

WebLorean was developed and tested on Ubuntu Desktop 16.04 and 17.04. From
the Ubuntu repositories only __python3-selenium__ and __chromium-chromedriver__ will
be installed. The rest of the required python 3 modules (make sure you
use **pip3**, which you can get via __sudo apt install python3-pip__) can
be installed off requirements.txt, so, basically, under Ubuntu, run this:

```
cd /usr/local/src/weblorean
sudo apt install chromium-chromedriver python3-selenium xvfb python3-pip -y
sudo pip3 install -r requirements.txt
```

If you know what you are doing, you can install selenium and chromedriver
off PIP as well, but you might need to tweak WebLorean source and/or
specify special command line arguments. Selenium is, by itself, sometimes a
bit delicate.

## Usage

Make sure you __source fix_environment.sh__ if you are running Ubuntu!

```
cd weblorean
./weblorean.py http://www.example.org

# specify a custom chromedriver path
./weblorean.py --chromedriver-path /usr/lib/chromium-browser/chromedriver http://www.example.org
```

By default WebLorean looks for a `chromedriver` executable in the current directory.

## What about Windows Subsystem for Linux?

If you are using Ubuntu under Windows 10 / WSL, you can run all non-SELENIUM
based methods. I dont think xvfb+pyvirtualdisplay are still WSL compatible,
although chromium DOES work. YMMV.
