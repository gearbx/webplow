# WebPlow - CLI web crawler
**WebPlow is a CLI web crawler. It has the following features:**
  - URLs to search are specified by input parameter and / or standard input 
  - configurable local proxy usage support
  - configurable delay between requests
  - configurable search max depth
  - configurable filter for extracted resources to be in the specified domain only
  - configurable filter for extracted resources to be in the same domain as the page where they are found
  - the found links are sent to stdout and the errors to stderr streams

## Installation
Prerequisites: [Python3](https://www.python.org/downloads/), [Pip](https://pip.pypa.io/en/stable/installation/)
```
# Cd into the project directory ("webplow")
# Make the install script executable.
chmod u+x ./install.sh
# Run the install script. (installs the dependency Python packages and copies the Python script to /usr/local/bin)
./install.sh
```

## Usage
```
usage: webplow.py [-h] [--url URL] [--delay DELAY] [--proxy PROXY] [--certfile CERTFILE]
                  [--specificdomain SPECIFICDOMAIN] [--samedomain] [--maxdepth MAXDEPTH]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             an URL to probe.
  --delay DELAY         the delay between requests in seconds. (default 1)
  --proxy PROXY         the proxy to use. (default none)
  --certfile CERTFILE   the proxy certificate file to use. (default none)
  --specificdomain SPECIFICDOMAIN
                        probe only links belonging to this specific domain. (default none)
  --samedomain          probe only links that are in the same domain as the page where they are found. (default false)
  --maxdepth MAXDEPTH   the max depth in searching for links. (default 1)
```

## Examples
#### Crawl single link
```
webplow.py --url https://python.org
```

#### Crawl multiple links passed through the standard input
```
cat input.txt | webplow.py
echo 'https://example.com' | webplow.py
```
 
#### Go more than one level deep
```
webplow.py --maxdepth 2 --url https://example.com
```

#### Use local proxy running on port 8080 along with cert file
```
webplow.py --url https://example.com --proxy 127.0.0.1:8080 --certfile ./proxy.pem
```

#### Filter result to only links that belong to the same domain as the input link(s)
```
webplow.py --url https://python.org --samedomain
```

#### Filter result to only links that belong to the specified domain
```
webplow.py --url https://python.org --specificdomain pandas.pydata.org
``` 

#### Use custom 5s delay between requests.
```
webplow.py --delay 5 --url https://python.org
```

## Version: 1.0
