import sys
import bot

url = str(sys.argv[1])
breadth = int(sys.argv[2])
#print(url,breadth)

BOT = bot.Bot(url,breadth)
BOT.init_crawl(url)
BOT.save()
