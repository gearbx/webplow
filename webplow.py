#!/usr/bin/python3

import argparse
import requests
import sys
import time
import urllib.parse

from bs4 import BeautifulSoup
from collections import namedtuple
from typing import List, Tuple

_URL_PARAM_NAME = "--url"
_DELAY_PARAM_NAME = "--delay"
_PROXY_PARAM_NAME = "--proxy"
_DOMAIN_ONLY_PARAM_NAME = "--domainonly"
_PARSER = 'html.parser'
_RESOURCE_LINK = 'link'
_RESOURCE_SCRIPT = 'script'

_params = None

Params = namedtuple('Params',['url','delay','proxy', 'domainonly'])

def _load_params():
    parser = argparse.ArgumentParser()
    parser.add_argument(_URL_PARAM_NAME, help="an URL to probe.")
    parser.add_argument(_DELAY_PARAM_NAME, action="count", default=3, help="the delay between requests in seconds.")
    parser.add_argument(_PROXY_PARAM_NAME, help="the proxy to use.")
    parser.add_argument(_DOMAIN_ONLY_PARAM_NAME, action="store_true", help="flag that can be set to probe only for same domain links.")
    args = parser.parse_args()
    global _params
    _params = Params(args.url, args.delay, args.proxy, args.domainonly)  


def _get_absolute_url(url: str, scheme: str, netloc: str) -> str:
    if url.startswith("//"):
        new_scheme = "https://" if scheme == "https" else "http://"
        return new_scheme + url[2:]
    
    if url.startswith("/"):
        return scheme + "://" + netloc + url

    return url


def _has_acceptable_domain(url:str, domain_to_have:str) -> bool:
    if not domain_to_have:
        return True
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    return domain == domain_to_have


def _get_attribute_values_for_nodes(data: BeautifulSoup, node_name: str, attribute_name: str) -> List[str]:
    values = []
    for node in data.find_all(node_name):
        attribute_value = node.get(attribute_name)
        if not attribute_value is None:
            values.append(attribute_value)
    return values


def _get_resources(url: str) -> List[Tuple[str, str]]:
    resources = []
    
    parsed_url = urllib.parse.urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    
    proxies = {
        'http': _params.proxy,
        'https': _params.proxy,
    }

    try:
        response = requests.get(url, proxies=proxies)
    except Exception as ex:
        print(f"Exception: {ex} retrieving {url}.", file=sys.stderr)
        return resources

    data = BeautifulSoup(response.text, _PARSER)

    expected_domain_for_found_resources = netloc if _params.domainonly else None

    for link in _get_attribute_values_for_nodes(data, 'a', 'href'):
        if link.startswith("#"):
            continue
        absolute_url = _get_absolute_url(link, scheme, netloc)
        if _has_acceptable_domain(absolute_url, expected_domain_for_found_resources):      
            resources.append((absolute_url, _RESOURCE_LINK))

    for script in _get_attribute_values_for_nodes(data, 'script', 'src'):
        absolute_url = _get_absolute_url(script, scheme, netloc)
        if _has_acceptable_domain(absolute_url, expected_domain_for_found_resources):      
            resources.append((absolute_url, _RESOURCE_SCRIPT))

    return resources


def main():
    _load_params()
    links_to_visit = []
    already_visited_links = set()

    if _params.url:        
        links_to_visit.append(_params.url)

    links_to_visit.extend([line.rstrip() for line in sys.stdin if line.rstrip()])

    while any(links_to_visit):
        link_to_visit = links_to_visit.pop(0)
        if not link_to_visit in already_visited_links:
            already_visited_links.add(link_to_visit)
            found_resources = _get_resources(link_to_visit)
            for found_link, resource_type in found_resources:
                if resource_type == _RESOURCE_LINK and found_link not in already_visited_links:
                    links_to_visit.append(found_link)
                print(f"{found_link} {resource_type}")
            time.sleep(_params.delay)

if __name__ == "__main__":
    main()
