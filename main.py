import sys
import bot
import utility

url = str(sys.argv[1])
breadth = int(sys.argv[2])
#print(url,breadth)

BOT = bot.Bot(url,breadth)
BOT.init_crawl(url)
utility.save_urls(BOT.get_crawled_urls())
