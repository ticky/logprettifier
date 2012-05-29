#!/usr/bin/env python

# logprettifier.py
# Takes source control logs and turns them into either Markdown (Default)
# or JSON for further processing or use in web apps.

import dateutil.parser
import json
import pytz
import sys
from xml.dom import minidom

# TODO: Make this return a nicely-formatted string, rather than print directly
def print_markdown(logData):
	for entry in logData:
		# TODO: Do a better job of dealing with special characters and newlines
		tmpdate = dateutil.parser.parse(entry["date"])
		print (
			'\n### r*%(revision)s*: **%(logMessage)s**' %
			{
				"revision":		entry["changeset"],
				"logMessage":	entry["message"].replace("*", "\\*").replace("\n"," ")
			}
		).encode('utf-8')

		print (
			'Submitted by %(author)s on %(date)s.\n' %
			{
				"author":	entry["author"],
				"date":		tmpdate.astimezone(pytz.timezone('Australia/Melbourne')).strftime("%A, %d %B %Y at %H:%M:%S (%Z)")
			}
		).encode('utf-8')

		for change in entry["files"]:

			fileActions = {
					"A":	"Added",
					"D":	"Deleted",
					"M":	"Modified",
					"R":	"Replaced"
			}

			print ('* %(action)s `%(file)s`' % {"action": fileActions.get(change["action"]), "file": change["file"]}).encode('utf-8')

# TODO: Make this usable as an option
def print_json(logData):
	return json.dumps(logData)

# TODO: Handle missing/malformed string portions in the parse function
def parse_svn_xml(file_path):

	dom = minidom.parse(file_path)

	svnLogObject = []

	for entry in dom.getElementsByTagName('logentry'):

		if(entry.getElementsByTagName('msg').item(0).firstChild):

			svnLogObject.append({
				"changeset":	entry.getAttribute('revision'),
				"message":		entry.getElementsByTagName('msg').item(0).firstChild.nodeValue,
				"author":		entry.getElementsByTagName('author').item(0).firstChild.nodeValue,
				"date":			entry.getElementsByTagName('date').item(0).firstChild.nodeValue,
				"files":		[]
			})

			for fileNode in entry.getElementsByTagName('path'):

				svnLogObject[-1]["files"].append({
					"action":	fileNode.getAttribute('action'),
					"file":		fileNode.firstChild.nodeValue
				})

	return svnLogObject

# TODO: Make this run happily in a CGI environment

if(len(sys.argv) > 1):
	# TODO: handle this (And switching modes!) more elegantly
	#		http://docs.python.org/library/argparse.html
	print(print_markdown(parse_svn_xml(sys.argv[1])))
else:
	# TODO: Print help?
	print('# Error')
	print('No arguments passed! Please give me a log file to parse.')