# Log Prettifier
A tool to create a day-by-day log of activity

## Requirements
 * Python 2.x (Made with 2.7, YMMV)
 * A web server capable of running Python scripts via CGI
 * Some event source you want to monitor. Current types are SVN and git
   repositories but the plan is to make it as extensible as possible.

## Installation
 * Clone repository into a web-facing directory on your server.
 * Edit configuration file to point at your event sources
     * git sorces require a local working directory. This does not need to be
       active, but must have the remote repository configured. Prettifier only
       fetches changes and will not merge them into your working copy (if any).
 * Visit page, be in awe.