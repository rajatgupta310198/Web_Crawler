import sys
import bot

url = 'http://iiitnr.ac.in/'

BOT = bot.Bot(url)
BOT.crawl(url)
BOT.save()