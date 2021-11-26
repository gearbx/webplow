# WebPlow
WebPlow is a CLI web crawler.
It has the following features:
  - urls to search are specified by input parameter and / or standard input.  
  - configurable local proxy usage support
  - configurable delay between requests
  - configurable search max depth
  - configurable filter found resources to be within the specified domain only


## Usage
```
usage: webplow.py [-h] [--url URL] [--delay] [--proxy PROXY] [--domainonly] [--maxdepth]

optional arguments:
  -h, --help     show this help message and exit
  --url URL      an URL to probe.
  --delay        the delay between requests in seconds. (default 1)
  --proxy PROXY  the proxy to use. (default none)
  --domainonly   flag that can be set to probe only for same domain links. (default false)
  --maxdepth     the max depth in searching for links. (default 1)
```
