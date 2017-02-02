from collections import deque
from urllib.request import urlopen
from urllib import error
from utility import MyParser


class Bot():
    def __init__(self,url,breadth=5):
        self.url = url # crwaling url
        self.visited_urls = set()
        self.base_url = url
        self.inQ_urls = deque([])
        self.breadth  = breadth

    def init_crawl(self,url):
        self.crawl(url)
        print('completed crwaling...', self.base_url)

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
        	#print('completed crwaling...', self.base_url)
        	return


    def save(self):
        with open('file.txt','wb') as fp:
            for i in self.visited_urls:
                x = i
                fp.write(x + '\n')

        fp.close()

