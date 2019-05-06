import scrapy
# from scrapy.crawler import CrawlerProcess

class SpiderDude(scrapy.Spider):
	""" Spider class for crawl all datacamp courses and extract the title and number of participants for each course """
	name = 'spider_dude'

	# to specify the output format and name
	custom_settings = {
		'FEED_URI': "[%(name)s]-datacamp_%(time)s.json",
		'FEED_FORMAT': 'json'
	}

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
		print("==++== Processing {} ==++==".format(response.url))
		# navigate to the html element containing the course title
		title = response.xpath('//h1[contains(@class, "title")]/text()').getall()
		# navigate to the html element containing time until completion
		time = response.css('li.header-hero__stat--hours::text').getall()
		# navigate to the html element containing the number of the course's videos
		video = response.css('li.header-hero__stat--videos::text').getall()
		# navigate to the html element containing the  number of the course's exercises
		exercise = response.css('li.header-hero__stat--exercises::text').getall()
		# navigate to the html element containing the number of audience
		audience = response.css('li.header-hero__stat--participants::text').getall()
		# navigate to the html element containing the trainers of the course
		trainer = response.css('h5.course__instructor-name::text').getall()
		# navigate to the html element containing the occupation of the trainers
		trainer_occupation = response.css('p.course__instructor-occupation::text').getall()
		# navigate to the html element containing the description of the trainers
		trainer_description = response.css('p.course__instructor-description::text').getall()
		# navigate to the html element containing the prerequisite of the course
		# prerequisite = response.css('li.course__prerequisite ::text').getall()

		# data reformation to extract only the numbers
		ti = "".join(map(str,time))
		time = int(ti[:-6])

		vi = "".join(map(str,video))
		video = int(vi[:-7])

		ex = "".join(map(str,exercise))
		exercise = int(ex[:-10])

		au = "".join(map(str,audience))
		au = "".join(c for c in au if c not in " ,")
		audience = int(au[:-12])

		number_of_trainer = len(trainer)

		# zip it to combine it all
		# row_data = zip(title, time, video, exercise, audience, total_trainer, trainer, trainer_occupation, trainer_description)

		# making the extracted data row-wise
		# for item in row_data:
		# 	data = {
		# 	'title': item[0],
		# 	'time': item[1],
		# 	'video': item[2],
		# 	'exercise': item[3],
		# 	'audience': item[4],
		# 	'total_trainer': item[5],
		# 	'trainer': item[6],
		# 	'trainer_occupation': item[7],
		# 	'trainer_description': item[8]
		# 	}

		# manual assignment of the extracted data
		data = {
		'title':title[0],
		'time':time,
		'video':video,
		'exercise':exercise,
		'audience':audience,
		'number_of_trainer':number_of_trainer,
		}

		for i in range(len(trainer)):
			data['trainer-'+str(i+1)] = trainer[i],
			data['trainer_occupation-'+str(i+1)] = trainer_occupation[i],
			data['trainer_description-'+str(i+1)] = trainer_description[i]

			yield data

		# ======================= This line below is to save the output using native python command, not using scrapy method ==============
		# data = time + ';' + audience

		# # store it in dictionary
		# data_dict[title] = data

# initialize the dict
# data_dict = dict()

# process = CrawlerProcess()
# process.crawl(SpiderDude)
# process.start()

# # initialize empty string
# text = ''

# for title, data in data_dict.items():
# 	text += title + ';' + data + '\n'

# filename = 'datacamp_audience.txt'
# with open(filename, 'w') as f:
# 	f.write(text)
