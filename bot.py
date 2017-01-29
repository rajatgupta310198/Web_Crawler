from html.parser import HTMLParser
from collections import deque
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib import parse

class Bot():
    def __init__(self,url):
        self.url = url # crwaling url
        self.visited_urls = []
        self.base_url = url
        self.inQ_urls = deque([])


    def crawl(self,url):
        self.visited_urls.append(self.url)
        response = urlopen(self.url)
        html_bytes = response.read()
        html = html_bytes.decode("utf-8")
        myparser = MyParser(self.url,self.url)
        myparser.feed(html)
        dis_links = myparser.get_links()
        for i in dis_links:
            self.inQ_urls.append(i)

        self.url = self.inQ_urls.popleft()
        self.crawl(self.url)

    def save(self):
        s = MyParser()
        s.feed(self.base_url)
        name = s.get_name()
        with open(name,'wb') as fp:
            for i in self.visited_urls:
                fp.write(i)

        fp.close()

class MyParser(HTMLParser):

    def __init__(self,base_url,page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.linlks_dis = set()
        self.title = ' '

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attr,value) in attrs:
                if attr == 'href':
                    url  = parse.urljoin(self.base_url,value)
                    self.linlks_dis.add(url)
                    print(url)



    def get_links(self):
        return self.linlks_dis


    def get_name(self):
        o = urlparse(self.base_url)
        self.title = o.fragement
        return self.title

