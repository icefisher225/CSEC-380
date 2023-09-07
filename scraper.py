import math, time, argparse, requests, re, typing
from os import link
from operator import is_
from dataclasses import dataclass
from bs4 import BeautifulSoup as bs
import multiprocessing as mp
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


def start_scraping(links, domain, maxdepth):
    mp.set_start_method("spawn")
    procs = []
    # Queue of links to scrape...
    toScrape = mp.Queue()

    # Queue of links returned
    retQueue = mp.Queue()

    for i in range(10):
        p = mp.Process(
            target=scrape_link,
            args=(
                toScrape,
                retQueue,
            ),
        )
        p.start()
        procs.append(p)

    while True:  # TODO: Condition????
        newLink = retQueue.get()
        if newLink not in links:
            if newLink.depth < maxdepth and newLink.url.startswith(domain):
                links.append(newLink)
                toScrape.put(newLink)
        if retQueue.is_empty():
            if toScrape.is_empty():
                break

    for p in procs:
        p.terminate()

    print(links)


def scrape_link(link, lst):
    foo = [_ for _ in parse(requests.get(link.url), link.depth)]
    for _ in foo:
        # print(_)
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

    print(f"Domain: {domain}\nStarting URL: {url.url}\nMax Depth: {maxdepth}")

    # Begin at url, scrape for all links/resources in HTML, CSS, and JS. Record all links/resources found under the domain.
    # Multithread the scraping process to speed up the process.
    # Do breadth first search for ease of removing duplicate links

    # exp = re.compile("""(href=").*?">""") # regex for parsing out URLs if necessary

    urls = []
    urls.append(url)

    # parsed = parse(requests.get(url.url), url.depth)

    # [urls.append(_) for _ in parsed if _ not in urls and _.url.startswith(domain)]

    # At this point, urls contains all links with depth 0 and have been deduplicated
    # Now we need an iterative or recursive solution to parse the rest

    curdepth = 0
    parsed = []
    curtime = time.time()
    while curdepth < maxdepth:
        threads = []
        for link in urls:
            # print(
            #    f"current depth: {curdepth}, link depth: {link.depth}, link: {link.url}"
            # )
            if link.depth == curdepth:
                t = Thread(
                    target=scrape_link,
                    args=(
                        link,
                        parsed,
                    ),
                )
                threads.append(t)
                time.sleep(0.02)
                t.start()
                if curdepth == 0:
                    time.sleep(2)
                # print(parsed)
        for t in threads:
            t.join()
        [urls.append(_) for _ in parsed if _ not in urls and _.url.startswith(domain)]
        curdepth += 1
        print(f"Time elapsed: {time.time() - curtime}\nDepth: {curdepth}")
    for item in urls:
        print(item.url, item.depth)

    print(f"Number of links after cleaning: {len(urls)}")
    print(f"Time elapsed: {time.time() - curtime}")

    """
    # Create a list of all links found
    links = mp.Queue()
    links.put(url)
    start_scraping(links, domain, maxdepth)
    """


if __name__ == "__main__":
    main()
