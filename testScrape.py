import scrapy
from scrapy.crawler import CrawlerProcess
# from scrapy import Selector
# import requests

# url = "https://www.datacamp.com/courses/all"
# html = requests.get(url).content

# sel = Selector(text=html)

# lists = sel.xpath('//p')

# # print(lists[:2].extract())

# title = sel.css('html>head>title::text')
# print("=====TITLE=====")
# print(title.extract_first())

# links = sel.css('div.course-block a::attr(href)').extract()
# titles = sel.css('div.course-block h4::text').extract()
# print("=====Links and Course Titles=====\n")
# for i in range(len(links)):
# 	print(titles[i], " || ", links[i])
# # for item in titles:
# # 	print(item)
# print(len(links))
# print(len(titles))

class SpiderMan(scrapy.Spider):
	""" A crawler class to collect all the course titles and their chapter titles from datacamp website """
	name = 'spider_man'

	def start_requests(self):
		urls = ["https://www.datacamp.com/courses/all"]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse_links)

	def parse_links(self, response):
		# navigate into the html element containing all the courses links
		links = response.css('div.course-block a::attr(href)').extract()
		for url in links:
			yield response.follow(url=url, callback=self.parse_pages)

	def parse_pages(self, response):
		# navigate into the html element containing the course title
		course_title = response.xpath('//h1[contains(@class, "title")]/text()')
		# extract and clean
		course_titles = course_title.extract_first().strip()
		# navigate into the html element containing the chapter titles
		chapter_title = response.css('h4.chapter__title::text')
		# extract and clean
		chapter_titles = [c.strip() for c in chapter_title.extract()]

		# filename = 'datacamp.csv'
		# with open(filename, 'w') as f:
			# f.writelines([c.strip() + "\n" for c in chapter_title.extract()])

		# store it in dictionary
		chapter_dict[course_titles] = chapter_titles

# initialize the dictionary
chapter_dict = dict()

# run the spider
process = CrawlerProcess()
process.crawl(SpiderMan)
process.start()

text = ""
filename = 'datacamp.csv'
for key, value in chapter_dict.items():
	chaps = ""
	for item in value:
		chaps += item + ";"
	text += key + " || " + chaps + "\n"
# write it into a file
with open(filename, 'w') as f:
	f.write(text)