from collections import deque
from urllib.request import urlopen
from urllib import error
from bs4 import BeautifulSoup
from utility import save_urls,save_scrap


def is_valid_url(url):
    try:
        resp = urlopen(url)
        return 1
    except error.URLError:
        return 0


class Bot():
    def __init__(self,url,breadth=5):
        self.url = url # crwaling url
        self.visited_urls = set()
        self.base_url = url
        self.inQ_urls = deque([])
        self.breadth  = breadth

    def init_crawl(self,url):
        if is_valid_url(url) == 0:
            print("Invalid URL " + str(url))
            exit()
        self.crawl(url)
        print('completed crwaling...', self.base_url)


    def crawl(self,url):
        try:
            response = urlopen(self.url).read()
            self.visited_urls.add(url)
            self.breadth -= 1
            if self.breadth == 0:
                self.inQ_urls.clear()
                return


            html = response.decode("utf-8")
            soup = BeautifulSoup(html,"html.parser")
            for i in soup.find_all('a'):
                self.inQ_urls.append(i.get('href'))


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

    def get_crawled_urls(self):
        return self.visited_urls

    def scrape_page(self,url):
        if is_valid_url(url) == 0:
            print('Invalid URL' + str(url))
            return

        html = urlopen(url).read()
        soup = BeautifulSoup(html,"html.parser")
        #print(soup.title.string)
        title = soup.title.string
        p_data = []
        for p_tag in soup.find_all('p'):
            p_data.append(str(p_tag.text))

        data = " ".join(p_data)
        save_scrap(title,data)
        return


if __name__ == "__main__":
    url = input("Enter URL:")
    #breadth = int(input("Enter breadth :"))
    bt = Bot(url,2)
    bt.scrape_page(url)
    #save_urls(bt.get_crawled_urls())

