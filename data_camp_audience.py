import scrapy
from scrapy.crawler import CrawlerProcess

class SpiderDude(scrapy.Spider):
	""" Spider class for crawl all datacamp courses and extract the title and number of participants for each course """
	name = 'spider_dude'

	def start_requests(self):
		urls = ["https://www.datacamp.com/courses/all"]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse_links)

	def parse_links(self, response):
		# navigate into the html element containing all the courses links
		links = response.css('div.course-block a::attr(href)').extract()
		for link in links:
			yield response.follow(url=link, callback=self.parse_pages)

	def parse_pages(self, response):
		# navigate to the html element containing the course title
		title = response.xpath('//h1[contains(@class, "title")]/text()').extract_first().strip()
		# navigate to the html element containing the number of audience
		audience = response.css('li.header-hero__stat--participants::text').extract_first()[:-13]
		# navigate to the html element containing time until completion
		time = response.css('li.header-hero__stat--hours::text').extract_first().strip()[:-6]

		# filename = 'datacamp_audience.csv'
		# with open(filename, 'w') as f:
		# 	f.writelines(title + ";" + time[:-6] + "\n")

		data = time + ';' + audience

		# store it in dictionary
		data_dict[title] = data

# initialize the dict
data_dict = dict()

process = CrawlerProcess()
process.crawl(SpiderDude)
process.start()

# initialize empty string
text = ''

for title, data in data_dict.items():
	text += title + ';' + data + '\n'

filename = 'datacamp_audience.txt'
with open(filename, 'w') as f:
	f.write(text)
