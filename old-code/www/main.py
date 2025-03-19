from bottle import route, static_file, template, redirect, get, post, request, response
import time
import datetime

def routes(app):
	# Home page
	@app.route('/')
	def index():

		loginfail = request.query.loginfail

		if loginfail == "" or loginfail is None:
			loginfail = 0
		elif loginfail == "1" or loginfail == 1:
			loginfail = 1
		else:
			loginfail = 2

		return template('login', loginfail=loginfail)

	# Login Logic
	@app.route('/login', method="POST")
	def index():
		if not request.forms.get('username') or not request.forms.get('password'):
			redirect('/?loginfail=1')

		username = request.forms.get('username')
		password = request.forms.get('password')

		if username == "jsovine" and password == "t7Tkm43.":
			redirect('/dashboard')
		elif username == "admin" and password == "grabreports2013!":
			redirect('/dashboard')
		else:
			redirect('/?loginfail=2')


	# Dashboard
	@app.route('/dashboard')
	def index():
		if not is_logged_in():
			redirect('/')
		else:
			return template('dashboard')

	# View Reports
	@app.route('/reports')
	def index(db):
		if not is_logged_in():
			redirect('/')

		db.execute("SELECT * FROM reports WHERE status IS NOT NULL OR status != '' ORDER BY id DESC LIMIT 100")
		currentReports = db.fetchall()

		db.execute("SELECT * FROM reports WHERE status IS NULL OR status = '' ORDER BY id DESC LIMIT 100")
		reports = db.fetchall()
		
		if reports:
			return template('reports', reports=reports, currentReports=currentReports, datetime=datetime)

	# Search for Reports
	@app.route('/reports/search', method='POST')
	def index(db):
		if not is_logged_in():
			redirect('/')

		if not request.forms.get('firstName') or not request.forms.get('lastName'):
			redirect('/reports')

		firstName = request.forms.get('firstName')
		lastName = request.forms.get('lastName')

		db.execute("SELECT * FROM reports WHERE first_name = %s AND last_name = %s LIMIT 10", [firstName, lastName])
		reports = db.fetchall()
		
		if reports:
			return template('reports_search', reports=reports, datetime=datetime)
		else:
			redirect('/reports')

	# Edit Report Data
	@app.route('/reports/edit/:id')
	def index(db, id):
		if not is_logged_in():
			redirect('/')

		if not id:
			redirect('/reports')

		error = request.query.error
		success = request.query.success

		if error == "" or error is None:
			error = 0
		else:
			error = 1

		if success == "" or success is None:
			success = 0
		else:
			success = 1

		db.execute("SELECT * FROM reports WHERE id = %s", [id,])
		report = db.fetchone()

		db.execute("SELECT * FROM users WHERE active = 1 ORDER BY last_name ASC")
		handlers = db.fetchall()

		db.execute("SELECT * FROM report_status ORDER BY weight ASC")
		statuses = db.fetchall()
		
		if report:
			return template('reports_edit', report=report, datetime=datetime, id=id, handlers=handlers, statuses=statuses, error=error, success=success)
		else:
			redirect('/reports?error=findreport')

	# Edit Report Data
	@app.route('/reports/edit/submit', method="POST")
	def index(db):
		if not is_logged_in():
			redirect('/')

		if not request.forms.get('id'):
			redirect('/reports')

		reportId = request.forms.get('id')
		handler = request.forms.get('handler')
		status = request.forms.get('status')
		firstNameUnit1 = request.forms.get('firstNameUnit1')
		lastNameUnit1 = request.forms.get('lastNameUnit1')
		firstNameUnit2 = request.forms.get('firstNameUnit2')
		lastNameUnit2 = request.forms.get('lastNameUnit2')

		if status == "Complete":
			dateTimeFinished = time.mktime(datetime.datetime.now().timetuple())
		else:
			dateTimeFinished = ""

		if db.execute("UPDATE reports SET handler = %s, status = %s, first_name = %s, last_name = %s, first_name_2 = %s, last_name_2 = %s, datetime_finished = %s WHERE id = %s", (handler, status, firstNameUnit1, lastNameUnit1, firstNameUnit2, lastNameUnit2, dateTimeFinished, reportId)):
			redirect("/reports/edit/%s?success=1" % reportId)
		else:
			redirect("/reports/edit/%s?error=1" % reportId)

	# View Report
	@app.route('/reports/view/:id')
	def index(db, id):
		if not is_logged_in():
			redirect('/')

		db.execute("SELECT local_link FROM reports WHERE id = %s", [id,])
		report = db.fetchone()

		if report:
			redirect('%s' % report["local_link"])
		else:
			redirect('/reports/?error=findreport')

	# View Sources
	@app.route('/sources')
	def index():
		if not is_logged_in():
			redirect('/')
			
		return template('sources')

	# View Members
	@app.route('/members')
	def index():
		if not is_logged_in():
			redirect('/')
			
		return template('members')

	# View User Settings
	@app.route('/settings')
	def index():
		if not is_logged_in():
			redirect('/')
			
		return template('settings')

	# Logout Logic
	@app.route('/logout')
	def index():
		if not is_logged_in():
			redirect('/')
		else:
			'''Destroy session'''
			redirect('/')
		
	# Static files
	@app.route('/images/<filename:path>')
	def image(filename):
		root = '/srv/service/grabreports/www/static/images'
		return static_file(filename, root=root)

	@app.route('/js/<filename:path>')
	def javascript(filename):
		root = '/srv/service/grabreports/www/static/js'
		return static_file(filename, root=root)

	@app.route('/css/<filename:path>')
	def stylesheet(filename):
		root = '/srv/service/grabreports/www/static/css'
		return static_file(filename, root=root)

	@app.route('/fonts/<filename:path>')
	def stylesheet(filename):
		root = '/srv/service/grabreports/www/static/fonts'
		return static_file(filename, root=root)

	@app.route('/reports/<filename:path>')
	def download(filename):
		root = '/srv/service/grabreports/reports'
		return static_file(filename, root=root)


	#@app.route('/reports/<filename:path>')
	#def download(filename):
	#   root = '/srv/service/grabreports/www/grabreports/reports'
	#   return static_file(filename, root=root, download=True)

def is_logged_in():
	return True
