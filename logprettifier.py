#!/usr/bin/env python

# logprettifier.py
# Takes source control logs and turns them into either Markdown (Default)
# or JSON for further processing or use in web apps.

# Parameters (Not yet implemented)
# - repo: the repo name specified in the config file. A shortcut to a username and password combination, essentially.
# - url: the URL of the repository to scan
# - username: the username to use on the repository
# - password: the password to use on the repository

import dateutil.parser
import json
import pytz
import sys
import subprocess
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

def get_svn_data():

    svnProcess = subprocess.Popen(['/usr/bin/svn', 'log', '--xml', '-l', '500', '-v', 'http://source.colloquy.info/svn/trunk'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, errors = svnProcess.communicate()

    dom = minidom.parseString(output)

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
# print "Content-Type: text/html"
print "Content-Type: application/json"
# CGI: Blank Line to separate Headers and Content
print ""
# CGI: Output
svnData = get_svn_data()
print(get_json(svnData))
