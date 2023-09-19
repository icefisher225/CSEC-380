"""
Ryan Cheevers-Brown
CSEC-380 Assignment 1 - Web Scraper
Written with a small amount of help from GitHub CoPilot. ~97% of code is human-generated. 
"""

import time, argparse, requests, re
from dataclasses import dataclass
from bs4 import BeautifulSoup as bs
from threading import Thread


@dataclass
class Link:
    url: str
    depth: int

    def __in__(self):
        return self.url


def get_args():
    parser = argparse.ArgumentParser(
        prog="CSEC 380 Web Scraper",
        description="Scrapes a web site for links and resources",
        epilog="Ryan Cheevers-Brown, c. 2023",
    )

    parser.add_argument(
        "-D", "--domain", type=str, required=True, help="Domain to scrape"
    )
    parser.add_argument(
        "-u", "--url", type=str, required=True, help="URL to begin scraping on"
    )
    parser.add_argument("-d", "--depth", type=int, default=0, help="Depth to scrape")

    return parser.parse_args()


def scrape_link(link, lst):
    foo = [_ for _ in parse(requests.get(link.url), link.depth)]
    for _ in foo:
        #print(_)
        lst.append(_)


def parse(response, curdepth):
    # parse the HTML response for links via href (all html links??? unsure)
    # return a list of links found
    soup = bs(response.text, "html.parser")
    links = []
    for link in soup.find_all(href=re.compile("^(http|https)://")):
        # return the new links in a list, increment depth by 1
        links.append(Link(link.get("href"), curdepth + 1))
    return links


def main():
    # start by getting the arguments
    args = get_args()

    domain = args.domain
    url = Link(args.url, 0)
    maxdepth = args.depth

    # print(f"Domain: {domain}\nStarting URL: {url.url}\nMax Depth: {maxdepth}")

    # Begin at url, scrape for all links/resources in HTML, CSS, and JS. Record all links/resources found under the domain.
    # Multithread the scraping process to speed up the process.
    # Do breadth first search for ease of removing duplicate links

    # exp = re.compile("""(href=").*?">""") # regex for parsing out URLs if necessary

    urls = []
    urls.append(url)

    # At this point, urls contains all links with depth 0 and have been deduplicated
    # Now we need an iterative or recursive solution to parse the rest

    curdepth = 0
    parsed = []
    curtime = time.time()
    while curdepth < maxdepth:
        threads = []
        for link in urls:
            if link.depth == curdepth:
                t = Thread(
                    target=scrape_link,
                    args=(
                        link,
                        parsed,
                    ),
                )
                threads.append(t)
                t.start()
                if curdepth == 0:
                    time.sleep(2)
                # print(parsed)
        for t in threads:
            t.join()
        [urls.append(_) for _ in parsed if _ not in urls and _.url.startswith(domain)]
        curdepth += 1
        print(f"Time elapsed {time.time() - curtime} for depth {curdepth}")
    # for item in urls:
    #     print(item.url, item.depth)

    print(f"Number of links after cleaning: {len(urls)}")
    # print(f"Time elapsed: {time.time() - curtime}")

    with open("links.txt", "w") as f:
        for item in urls:
            f.write(f"{item.url}\n")

    time.sleep(10)

if __name__ == "__main__":
    main()
