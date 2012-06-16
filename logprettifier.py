#!/usr/bin/env python

# logprettifier.py
# Retrieves multiple source control logs, combines them and converts to JSON for
# further processing or use in web apps.

# Parameters (Not yet implemented)
# - repo: the repo name specified in the config file.
#         (Note: when unspecified, all enabled repos are fetched.)

# Timezone Utilities
import dateutil.parser
#import pytz

# System IO Utilities
import sys
import subprocess

# Serialisation Utilities
from xml.dom import minidom
import json

# CGI Utilities
import cgitb
cgitb.enable()

# TODO: Turn this into a class with constructors and useful OO things so it can
#       be re-used and expanded upon.
def get_svn_data():

    svnProcess = subprocess.Popen(
        [
            '/usr/bin/svn', 'log',
            '--xml',
            '-l', '500',
            '-v',
            'http://source.colloquy.info/svn/trunk'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
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

# TODO: Write a simple CGI wrapper allowing for a buffer to be written to before
#       flushing as response.
# CGI: Header(s)
print "X-Powered-By: Python"
# print "Content-Type: text/html"
print "Content-Type: application/json"
# CGI: Blank Line to separate Headers and Content
print ""

# CGI: Output
print(json.dumps(get_svn_data()))
