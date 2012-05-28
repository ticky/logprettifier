import dateutil.parser
import json
import pytz
import sys
from xml.dom import minidom

# TODO: Make this return a nicely-formatted string, rather than print directly.
def print_markdown(logData):
	for entry in logData:
		print ('\n### r*%(revision)s*: **%(logMessage)s**' % {"revision": entry["changeset"], "logMessage": entry["message"]}).encode('utf-8')
		print ('Submitted by %(author)s on %(date)s.\n' % {"author": entry["author"], "date": entry["date"]}).encode('utf-8')
		for change in entry["files"]:
			fileActions = {
					"A":	"Added",
					"D":	"Deleted",
					"M":	"Modified",
					"R":	"Replaced"
			}
			print ('* %(action)s `%(file)s`' % {"action": fileActions.get(change["action"]), "file": change["file"]}).encode('utf-8')

def print_json(logData):
	return json.dumps(logData)

def parse_svn_xml(file_path):

	dom = minidom.parse(file_path)

	svnLogObject = []

	for entry in dom.getElementsByTagName('logentry'):

		if(entry.getElementsByTagName('msg').item(0).firstChild):

			tmpdate = dateutil.parser.parse(entry.getElementsByTagName('date').item(0).firstChild.nodeValue)

			svnLogObject.append({
				"changeset":	entry.getAttribute('revision'),
				"message":		entry.getElementsByTagName('msg').item(0).firstChild.nodeValue,
				"author":		entry.getElementsByTagName('author').item(0).firstChild.nodeValue,
				"date":			tmpdate.astimezone(pytz.timezone('Australia/Melbourne')).strftime("%A, %d %B %Y at %H:%M:%S (%Z)"),
				"files":		[]
			})

			for fileNode in entry.getElementsByTagName('path'):

				svnLogObject[-1]["files"].append({
					"action":	fileNode.getAttribute('action'),
					"file":		fileNode.firstChild.nodeValue
				})

	return svnLogObject

if(len(sys.argv) > 1):
	# TODO: handle this (And switching modes!) more elegantly.
	print(print_markdown(parse_svn_xml(sys.argv[1])))
else:
	print('# Error')
	print('No arguments passed! Please give me a log file to parse.')