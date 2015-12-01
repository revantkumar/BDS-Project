import web
import json
import csv
import urllib2
import subprocess
import glob, os

urls = (
	'/fetch_comments', 'Fetch',
	'/test', 'Test'
)

class Fetch:
	def GET(self):
		user_data = web.input()
		url = user_data.url
		print url

		comment_urls = []

		response = urllib2.urlopen(url)
		cr = csv.reader(response)

		print "reading file"

		for row in cr:
			if len(comment_urls) is 100:
				break

			if (len(row) >= 35 and row[34].startswith('http://')):
				comment_urls.append(row[34])
		
		print len(comment_urls)
		self.extract_comments(comment_urls)
		return 'success'

	def extract_comments(self, comments_url):
		i = 1
		self.empty_dir('../comments')		
		for url in comments_url:
			print url
			res = subprocess.call(['/Users/anurag/study/SEM-3/bds/proj/opt/dataService/phantomjs-2.0.0-macosx/bin/phantomjs', '/Users/anurag/study/SEM-3/bds/proj/opt/dataService/test.js', url, str(i)])
			i += 1

		return None

	def empty_dir(self, path):
		os.popen('rm -f ' + path + '/*')

class Test:
        def GET(self):
		res = subprocess.call(['/Users/anurag/study/SEM-3/bds/proj/opt/dataService/phantomjs-2.0.0-macosx/bin/phantomjs', '/Users/anurag/study/SEM-3/bds/proj/opt/dataService/test.js', 'http://www.regulations.gov/#!documentDetail;D=ICEB-2015-0002-2258', ])
		print res
		return 'success'

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
