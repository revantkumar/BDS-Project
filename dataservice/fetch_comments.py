import web
import json
import csv
import urllib2
import subprocess
import os, os.path
import random

urls = (
	'/fetch_comments', 'Fetch',
	'/get_count', 'Count',
	'/get_top', 'Top'
)

class Fetch:
	def GET(self):
		user_data = web.input()
		url = user_data.url
		token = user_data.token
		print url

		comment_urls = []

		response = urllib2.urlopen(url)
		cr = csv.reader(response)

		print "reading file"
		index = 1

		for row in cr:
			if len(comment_urls) is 10000:
				break

			if index > 15000 and (len(row) >= 35 and row[34].startswith('http://')):
				comment_urls.append(row[34])

			index += 1

		print len(comment_urls)
		self.extract_comments(comment_urls, token)
		return 'success'

	def extract_comments(self, comments_url, token):
		i = 15000
		for url in comments_url:
			print url
			res = subprocess.call(['/Users/anurag/study/SEM-3/bds/proj/opt/dataService/phantomjs-2.0.0-macosx/bin/phantomjs', '/Users/anurag/study/SEM-3/bds/proj/BDS-Project/dataservice/test.js', url, str(i), token])

			if (i%5 is 0):
				subprocess.call('python ../backend.py comments/' + token + ' ' + token + ' /Users/anurag/study/SEM-3/bds/proj/BDS-Project', shell=True)

			i += 1

		return None

	def empty_dir(self, path):
		os.popen('rm -f ' + path + '/*')

class Count:
	def GET(self):
		DIR = '../comments'
		res = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
		return res

class Top:
	def GET(self):
		DIR = '../comments'
		paths = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
		contents = []
		res = []

		for path in paths:
			text_file = open('../comments/' + path, "r")
			whole_thing = text_file.read()
			contents.append(whole_thing)

		size = len(contents)
		print size
		if size < 100:
			return "~~".join(contents)
		else:
			for i in range(100):
				index = random.randint(0, size-1)
				print index
				res.append(contents[index])

			return "~~".join(res)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
