import urllib.request
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["crawlerdb"]
pages_collection = db["pages"]


class Frontier:
    def __init__(self):
        self.to_visit = []
        self.visited = set()
        self.done_flag = False

    def addURL(self, url):
        if url not in self.visited and url not in self.to_visit:
            self.to_visit.append(url)

    def nextURL(self):
        if self.to_visit:
            url = self.to_visit.pop(0)
            self.visited.add(url)
            return url
        else:
            return None

    def done(self):
        return self.done_flag or not self.to_visit

    def clear_frontier(self):
        self.to_visit = []
        self.done_flag = True


def retrieveHTML(url):
    try:
        response = urllib.request.urlopen(url)
        content_type = response.headers.get('Content-Type')
        if 'text/html' in content_type:
            html = response.read()
            return html
        else:
            return None
    except Exception as e:
        print(f"Failed to retrieve {url}: {e}")
        return None


def storePage(url, html):
    pages_collection.insert_one({'url': url, 'html': html.decode('utf-8')})


def parse(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Build absolute URL
        href = urljoin(base_url, href)
        # Only consider HTTP and HTTPS URLs
        parsed_href = urlparse(href)
        if parsed_href.scheme in ['http', 'https']:
            # Only considering the HTML and SHTML pages
            path = parsed_href.path
            if path.endswith('.html') or path.endswith('.shtml') or path.endswith('.htm') or path == '' or path.endswith('/'):
                # Only considering the URLs within the CS website
                if href.startswith('https://www.cpp.edu/sci/computer-science/'):
                    urls.append(href)
    return urls


def targetpage(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1', class_='cpp-h1')
    if h1 and h1.text.strip() == 'Permanent Faculty':
        return True
    return False


def flagTargetPage(url):
    print(f"Target page found: {url}")


def crawlerThread(frontier):
    while not frontier.done():
        url = frontier.nextURL()
        if url is None:
            break
        print(f"Visiting: {url}")
        html = retrieveHTML(url)
        if html:
            storePage(url, html)
            if targetpage(html):
                flagTargetPage(url)
                frontier.clear_frontier()
            else:
                urls = parse(html, url)
                for link in urls:
                    if link not in frontier.visited:
                        frontier.addURL(link)


if __name__ == "__main__":
    start_url = 'https://www.cpp.edu/sci/computer-science/'
    frontier = Frontier()
    frontier.addURL(start_url)
    crawlerThread(frontier)
