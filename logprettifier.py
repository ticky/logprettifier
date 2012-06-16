#!/usr/bin/env python

# logprettifier.py
# Takes source control logs and turns them into either Markdown (Default)
# or JSON for further processing or use in web apps.

import dateutil.parser
import json
import pytz
import sys
from xml.dom import minidom

def print_markdown(logData):

    markdownLog = []

    for entry in logData:

        # TODO: Do a better job of dealing with newlines (split then iterate?)
        tmpdate = dateutil.parser.parse(entry["date"])

        markdownLog.append(
            '### r*%(revision)s*: **%(logMessage)s**' %
            {
                "revision":     markdown_escape(entry["changeset"]),
                "logMessage":   markdown_escape(entry["message"])
            }
        )

        numFiles = len(entry["files"])
        if(numFiles == 1):
            fileStr = "%i file" % numFiles
        else:
            fileStr = "%i files" % numFiles

        markdownLog.append(
            '**%(author)s** modified **%(files)s** on **%(date)s**' %
            {
                "author":   markdown_escape(entry["author"]),
                "files":    markdown_escape(fileStr),
                "date":     markdown_escape(tmpdate.astimezone(pytz.timezone('Australia/Melbourne')).strftime("%A, %d %B %Y at %H:%M:%S (%Z)"))
            }
        )

        markdownLog.append('')

        for change in entry["files"]:

            fileActions = {
                    "A":    "Added",
                    "D":    "Deleted",
                    "M":    "Modified",
                    "R":    "Replaced"
            }

            markdownLog.append(
                '* %(action)s `%(file)s`' %
                {
                    "action":   fileActions.get(change["action"]),
                    "file":     change["file"]
                }
            )

        markdownLog.append('\n') # Put two newlines between this and the next entry.

    return '\n'.join(markdownLog).encode('utf-8')

# TODO: Make this usable as an option
def get_json(logData):

    return json.dumps(logData)

def markdown_escape(inputString):

    return inputString.replace("\\", "\\\\").replace("`","\\`").replace("*", "\\*").replace("_", "\\_").replace("-", "\\-").replace("+", "\\+").replace(".", "\\.").replace("!", "\\!")

# TODO: Handle missing/malformed string portions in the parse function
def parse_svn_xml(file_path):

    dom = minidom.parse(file_path)

    svnLogObject = []

    for entry in dom.getElementsByTagName('logentry'):

        if(entry.getElementsByTagName('msg').item(0).firstChild):

            svnLogObject.append({
                "changeset":    entry.getAttribute('revision'),
                "message":      entry.getElementsByTagName('msg').item(0).firstChild.nodeValue,
                "author":       entry.getElementsByTagName('author').item(0).firstChild.nodeValue,
                "date":         entry.getElementsByTagName('date').item(0).firstChild.nodeValue,
                "files":        []
            })

            for fileNode in entry.getElementsByTagName('path'):

                svnLogObject[-1]["files"].append({
                    "action":   fileNode.getAttribute('action'),
                    "file":     fileNode.firstChild.nodeValue
                })

    return svnLogObject

# CGI: Header(s)
print "X-Powered-By: Python"
# print "Content-Type: text/json"
# CGI: Blank Line to separate Headers and Content
print ""
# CGI: Output
print(get_json(parse_svn_xml('C:\\log.xml')))
=======
#!/usr/bin/env python

# logprettifier.py
# Takes source control logs and turns them into either Markdown (Default)
# or JSON for further processing or use in web apps.

import dateutil.parser
import json
import pytz
import sys
from xml.dom import minidom
import cgitb
cgitb.enable()

def print_markdown(logData):

    markdownLog = []

    for entry in logData:

        # TODO: Do a better job of dealing with newlines (split then iterate?)
        tmpdate = dateutil.parser.parse(entry["date"])

        markdownLog.append(
            '### r*%(revision)s*: **%(logMessage)s**' %
            {
                "revision":     markdown_escape(entry["changeset"]),
                "logMessage":   markdown_escape(entry["message"])
            }
        )

        numFiles = len(entry["files"])
        if(numFiles == 1):
            fileStr = "%i file" % numFiles
        else:
            fileStr = "%i files" % numFiles

        markdownLog.append(
            '**%(author)s** modified **%(files)s** on **%(date)s**' %
            {
                "author":   markdown_escape(entry["author"]),
                "files":    markdown_escape(fileStr),
                "date":     markdown_escape(tmpdate.astimezone(pytz.timezone('Australia/Melbourne')).strftime("%A, %d %B %Y at %H:%M:%S (%Z)"))
            }
        )

        markdownLog.append('')

        for change in entry["files"]:

            fileActions = {
                    "A":    "Added",
                    "D":    "Deleted",
                    "M":    "Modified",
                    "R":    "Replaced"
            }

            markdownLog.append(
                '* %(action)s `%(file)s`' %
                {
                    "action":   fileActions.get(change["action"]),
                    "file":     change["file"]
                }
            )

        markdownLog.append('\n') # Put two newlines between this and the next entry.

    return '\n'.join(markdownLog).encode('utf-8')

# TODO: Make this usable as an option
def get_json(logData):

    return json.dumps(logData)

def markdown_escape(inputString):

    return inputString.replace("\\", "\\\\").replace("`","\\`").replace("*", "\\*").replace("_", "\\_").replace("-", "\\-").replace("+", "\\+").replace(".", "\\.").replace("!", "\\!")

# TODO: Handle missing/malformed string portions in the parse function
def parse_svn_xml(file_path):

    dom = minidom.parse(file_path)

    svnLogObject = []

    for entry in dom.getElementsByTagName('logentry'):

        if(entry.getElementsByTagName('msg').item(0).firstChild):

            svnLogObject.append({
                "changeset":    entry.getAttribute('revision'),
                "message":      entry.getElementsByTagName('msg').item(0).firstChild.nodeValue,
                "author":       entry.getElementsByTagName('author').item(0).firstChild.nodeValue,
                "date":         entry.getElementsByTagName('date').item(0).firstChild.nodeValue,
                "files":        []
            })

            for fileNode in entry.getElementsByTagName('path'):

                svnLogObject[-1]["files"].append({
                    "action":   fileNode.getAttribute('action'),
                    "file":     fileNode.firstChild.nodeValue
                })

    return svnLogObject

# CGI: Header(s)
print "X-Powered-By: Python"
print "Content-Type: text/html"
# CGI: Blank Line to separate Headers and Content
print ""
# CGI: Output
print(get_json(parse_svn_xml('/Users/ticky/svnlog.xml')))
