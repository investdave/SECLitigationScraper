from BeautifulSoup import BeautifulSoup
import requests
import re
import os


def start():
	#list of starting URLS?
	startingURLS = ["http://www.sec.gov/litigation/litreleases.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2014.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2013.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2012.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2011.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2010.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2009.shtml"
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2008.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2007.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2006.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2005.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2004.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2003.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2002.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2001.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive2000.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive1999.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive1998.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive1997.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive1996.shtml",
	"http://www.sec.gov/litigation/litreleases/litrelarchive/litarchive1995.shtml"]
	for startingURL in startingURLS:
		r = requests.get(startingURL)
		soup = BeautifulSoup(r.text)
		relevantArticles = []
		for link in soup.findAll():
			if link.get('href') != None:
				if 'lr' in link.get('href') and 'htm' in link.get('href'):
					relevantArticles.append(link.get('href'))
		for article in relevantArticles:
			print article
			scrapper(article)

def scrapper(URL):
	fullURL = "http://www.sec.gov" + URL
	keywords = ["Section 10(b)", "Securities Exchange Act of 1934", "Insider"]
	r = requests.get(fullURL)
	soup = BeautifulSoup(r.text)
	for words in keywords:
		x = soup.body.findAll(text=re.compile(words))
		if bool(x):
			database(fullURL, soup)

def database(dataUrl, content):
	title = re.sub('[^\w\-_\. ]', '_', (content.title.text[0:15]))
	articleDownloadFilename = str(title) + '.htm'

	try:
		articleDownload = open((articleDownloadFilename), 'w')
		articleDownload.write(content.prettify("utf-8"))
		articleDownload.close()

	except:
		errorMSG = open("errors.txt", 'a')
		errorMSG.write("Can't write {} \n".format(dataUrl))
		errorMSG.close()

	try: 
		text = open("links.txt", 'a')
		fullText = "Article Name: {} Link: {} \n".format(content.title.text, dataUrl)
		text.write(fullText)
		text.close()

	except: 
		errorMSG = open("errors.txt", 'a')
		errorMSG.write("Can't write {} \n".format(dataUrl))
		errorMSG.close()

start()
