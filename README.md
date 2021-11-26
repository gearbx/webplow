# WebPlow
WebPlow is a CLI web crawler.

## Usage
`
usage: webplow.py [-h] [--url URL] [--delay] [--proxy PROXY] [--domainonly] [--maxdepth]

optional arguments:
  -h, --help     show this help message and exit
  --url URL      an URL to probe.
  --delay        the delay between requests in seconds. (default 1)
  --proxy PROXY  the proxy to use. (default none)
  --domainonly   flag that can be set to probe only for same domain links. (default false)
  --maxdepth     the max depth in searching for links. (default 1)
`
