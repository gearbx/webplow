# WebPlow
## Intro
WebPlow is a CLI web crawler.
It has the following features:
  - urls to search are specified by input parameter and / or standard input.  
  - configurable local proxy usage support
  - configurable delay between requests
  - configurable search max depth
  - configurable filter for extracted resources to be in the specified domain only
  - configurable filter for extracted resources to be in the same domain as the page where they are found
  - found links are sent to stdout, errors to stderr streams

## Install
Prerequisites: Python3, Pip
```
# Cd into the project directory ("webplow")
# Make the install script executable.
chmod u+x ./install.sh
# Run the install script.
./install.sh
```

## Usage
```
usage: webplow.py [-h] [--url URL] [--delay] [--proxy PROXY] [--specificdomain SPECIFICDOMAIN] [--samedomain] [--maxdepth]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             an URL to probe.
  --delay               the delay between requests in seconds. (default 1)
  --proxy PROXY         the proxy to use. (default none)
  --specificdomain SPECIFICDOMAIN
                        probe only extracted links belonging to this specific domain. (default none)
  --samedomain          probe only extracted links that are in the same domain as the page where they are found. (default false)
  --maxdepth            the max depth in searching for links. (default 1)
```
