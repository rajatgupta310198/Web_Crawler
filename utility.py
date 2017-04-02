from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib import parse


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
                if attr == 'href' and value != 'mailto:$' and value != 'tel:$':
                    url  = parse.urljoin(self.base_url,value)
                    #print(url)
                    self.linlks_dis.add(url)

    def get_links(self):
        return self.linlks_dis

    def get_name(self):
        o = urlparse(self.base_url)
        self.title = o.fragement
        return self.title


def save_urls(urls):
    f = open('file.txt',mode='w')
    for i in urls:
        f.write(i + '\n')

    f.close()

