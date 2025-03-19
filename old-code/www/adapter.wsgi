import os, sys, bottle, bottle_mysql
from beaker.middleware import SessionMiddleware

# Add app directory to PATH
sys.path.append(os.path.dirname(__file__))
# Change to app directory
os.chdir(os.path.dirname(__file__))

# Session data
session_opts = {
	'session.type': 'file',
	'session.cookie_expires': 300,
	'session.data_dir': './data',
	'session.auto': True
}

# Start bottle
#application = SessionMiddleware(bottle.default_app(), session_opts)

# Start bottle
application = bottle.default_app()

# dbhost is optional, default is localhost
plugin = bottle_mysql.Plugin(dbuser='grabreports', dbpass='GrabReports2012!', dbname='grabreports_dev')
application.install(plugin)

import main

# Start routing
main.routes(application)