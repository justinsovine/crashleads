from bottle import route, static_file, template

# Home page
@route('/')
def index(headline='GrabReports.com', tagline='Coming Soon!', cat=False):
		return template('home', headline=headline, tagline=tagline, cat=cat)

# Supreme ruler, "Cat"
@route('/cat')
def index(headline='GrabReports.com', tagline='Coming Soon!', cat=True):
		return template('home', headline=headline, tagline=tagline, cat=cat)

# Static files
@route('/images/<filename:path>')
def image(filename):
		root = '/srv/www/grabreports.com/www_static/images'
		return static_file(filename, root=root)

@route('/js/<filename:path>')
def javascript(filename):
		root = '/srv/www/grabreports.com/www_static/js'
		return static_file(filename, root=root)

@route('/css/<filename:path>')
def stylesheet(filename):
		root = '/srv/www/grabreports.com/www_static/css'
		return static_file(filename, root=root)

@route('/download/<filename:path>')
def download(filename):
		root = '/srv/www/grabreports.com/www_static/downloads'
		return static_file(filename, root=root, download=True)