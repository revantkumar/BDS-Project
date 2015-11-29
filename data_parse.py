import json

f = open('data.txt', 'r')
data = f.read()
data = json.loads(data)

print data[0]

for e in data:
	comment_id = e['id']
	if e['vote'] == 1:
		vote = 'Y'
	else:
		vote = 'N'
	comment = e['text']

	f1 = open("data/" + str(comment_id) + "-" + vote + ".txt", 'w')
	f1.write(comment.encode('utf-8'))
	f1.close()