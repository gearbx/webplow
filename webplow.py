#!/usr/bin/python3

import argparse
import requests
import sys
import time
import urllib.parse

from bs4 import BeautifulSoup
from collections import namedtuple
from typing import List, Tuple

_PARSER = 'html.parser'
_RESOURCE_LINK = 'link'
_RESOURCE_SCRIPT = 'script'
_BAD_INPUT_ERROR_CODE = 1

Params = namedtuple('Params',['url', 'delay', 'proxy', 'certfile', 'specificdomain', 'samedomain', 'maxdepth'])


def check_larger_than_zero(value):
    try:
        v = int(value)
        if v <= 0:
            print(f"Invalid parameter value {value}", file=sys.stderr)
            sys.exit(_BAD_INPUT_ERROR_CODE)
        return v
    except Exception:
        print(f"Invalid parameter value {value}", file=sys.stderr)
        sys.exit(_BAD_INPUT_ERROR_CODE)

def _get_loaded_params():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="an URL to probe.")
    parser.add_argument("--delay", type=check_larger_than_zero, default=1, help="the delay between requests in seconds. (default 1)")
    parser.add_argument("--proxy", default=None, help="the proxy to use. (default none)")
    parser.add_argument("--certfile", default=None, help="the proxy certificate file to use. (default none)")
    parser.add_argument("--specificdomain", default=None, help="probe only links belonging to this specific domain. (default none)")
    parser.add_argument("--samedomain", action="store_true", default=False, help="probe only links that are in the same domain as the page where they are found. (default false)")
    parser.add_argument("--maxdepth", type=check_larger_than_zero, default=1, help="the max depth in searching for links. (default 1)")
    args = parser.parse_args()
    return Params(args.url, args.delay, args.proxy, args.certfile, args.specificdomain, args.samedomain, args.maxdepth)  


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


def _get_resources(url: str, params: Params) -> List[Tuple[str, str]]:
    resources = []
    
    # get the resource data
    proxies = {
        'http': params.proxy,
        'https': params.proxy,
    }
    try:
        response = requests.get(url, proxies=proxies, verify=params.certfile)
    except Exception as ex:
        print(f"Exception: {ex} retrieving {url}.", file=sys.stderr)
        return resources

    # check domain filters
    parsed_url = urllib.parse.urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    expected_domain_for_found_resources = None
    if (params.samedomain):
        if (params.specificdomain):
            if (params.specificdomain == netloc):
                expected_domain_for_found_resources = netloc
            else:
                return resources
        else:
            expected_domain_for_found_resources = netloc
    else:
        expected_domain_for_found_resources = params.specificdomain

    # parse the response data
    data = BeautifulSoup(response.text, _PARSER)

    # extract links
    for link in _get_attribute_values_for_nodes(data, 'a', 'href'):
        if link.startswith("#"):
            continue
        absolute_url = _get_absolute_url(link, scheme, netloc)
        if _has_acceptable_domain(absolute_url, expected_domain_for_found_resources):      
            resources.append((absolute_url, _RESOURCE_LINK))

    # extract scripts
    for script in _get_attribute_values_for_nodes(data, 'script', 'src'):
        absolute_url = _get_absolute_url(script, scheme, netloc)
        if _has_acceptable_domain(absolute_url, expected_domain_for_found_resources):      
            resources.append((absolute_url, _RESOURCE_SCRIPT))

    return resources


def main():
    params = _get_loaded_params()
    links_to_visit_with_depth = []
    already_visited_links = set()

    if params.url:        
        links_to_visit_with_depth.append((params.url, 1))
    else:
        links_to_visit_with_depth.extend([(line.rstrip(), 1) for line in sys.stdin if line.rstrip()])

    while any(links_to_visit_with_depth):
        link_to_visit, depth = links_to_visit_with_depth.pop(0)
        if (depth <= params.maxdepth) and not link_to_visit in already_visited_links:
            already_visited_links.add(link_to_visit)
            found_resources = _get_resources(link_to_visit, params)
            for found_link, resource_type in found_resources:
                if resource_type == _RESOURCE_LINK and found_link not in already_visited_links:
                    links_to_visit_with_depth.append((found_link, depth + 1))
                print(f"{found_link} {resource_type}")
            time.sleep(params.delay)

if __name__ == "__main__":
    main()
