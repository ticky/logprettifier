import dateutil.parser
import pytz
import sys
from xml.dom import minidom

def markdown_log(file_path):

	dom = minidom.parse(file_path)

	for entry in dom.getElementsByTagName('logentry'):

		if(entry.getElementsByTagName('msg').item(0).firstChild):

			loginfo = {
				"revision":		entry.getAttribute('revision'),
				"logMessage":	entry.getElementsByTagName('msg').item(0).firstChild.nodeValue
			}

			tmpdate = dateutil.parser.parse(entry.getElementsByTagName('date').item(0).firstChild.nodeValue)

			subinfo = {
				"author":	entry.getElementsByTagName('author').item(0).firstChild.nodeValue,
				"date":		tmpdate.astimezone(pytz.timezone('Australia/Melbourne')).strftime("%A, %d %B %Y at %H:%M:%S (%Z)")
			}

			print ('\n### r*%(revision)s*: **%(logMessage)s**' % loginfo).encode('utf-8')
			print ('Submitted by %(author)s on %(date)s.\n' % subinfo).encode('utf-8')

			for fileNode in entry.getElementsByTagName('path'):

				fileActions = {
					"A":	"Added",
					"D":	"Deleted",
					"M":	"Modified",
					"R":	"Replaced"
				}

				fileinfo = {
					"action": fileActions.get(fileNode.getAttribute('action')),
					"file": fileNode.firstChild.nodeValue
				}

				print ('* %(action)s `%(file)s`' % fileinfo).encode('utf-8')

if(len(sys.argv) > 1):
	# TODO: handle this more elegantly.
	markdown_log(sys.argv[1])
else:
	print('# Error')
	print('No arguments passed! Please give me a log file to parse.')