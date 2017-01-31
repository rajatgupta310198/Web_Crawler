from html.parser import HTMLParser
from collections import deque
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib import parse
from urllib import error


class Bot():
    def __init__(self,url,breadth=5):
        self.url = url # crwaling url
        self.visited_urls = set()
        self.base_url = url
        self.inQ_urls = deque([])
        self.breadth  = breadth

    def crawl(self,url):
        self.visited_urls.add(url)
        self.breadth -= 1
        if self.breadth == 0:
            self.inQ_urls.clear()
            return
        print(self.visited_urls)
        try:
            response = urlopen(self.url)
            html_bytes = response.read()
            html = html_bytes.decode("utf-8")
            myparser = MyParser(self.base_url, self.url)
            myparser.feed(html)
            dis_links = myparser.get_links()
            for i in dis_links:
                self.inQ_urls.append(i)
        except error.HTTPError:
            self.url = self.inQ_urls.popleft()
            self.crawl(self.url)
        except error.URLError:
            self.url = self.inQ_urls.popleft()
            self.crawl(self.url)
        except UnicodeDecodeError:
            self.url = self.inQ_urls.popleft()
            self.crawl(self.url)

        except ValueError:
        	print('Unknow url :',self.url,'enter complete for e.g http://exapmle.com')
        	exit()

        except IndexError:
        	print('Completed..')

        try:
        	self.url = self.inQ_urls.popleft()
        	self.crawl(self.url)

        except IndexError:
        	print('completed crwaling...', self.base_url)
        	return


    def save(self):
        s = MyParser(self.base_url,self.base_url)
        s.feed(self.base_url)
        with open('file.txt','wb') as fp:
            for i in self.visited_urls:
                fp.write(i+"\n")

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
                if attr == 'href' and value != 'mailto:$':
                    url  = parse.urljoin(self.base_url,value)
                    #print(url)
                    self.linlks_dis.add(url)

    def get_links(self):
        return self.linlks_dis

    def get_name(self):
        o = urlparse(self.base_url)
        self.title = o.fragement
        return self.title

