% include header title="Edit Crash Report"

% if report:
% 	firstNameUnit1 = report["first_name"]
%	if firstNameUnit1 is None:
%		firstNameUnit1 = ""
%	end

% 	lastNameUnit1 = report["last_name"]
%	if lastNameUnit1 is None:
%		lastNameUnit1 = ""
%	end

% 	firstNameUnit2 = report["first_name_2"]
%	if firstNameUnit2 is None:
%		firstNameUnit2 = ""
%	end

% 	lastNameUnit2 = report["last_name_2"]
%	if lastNameUnit2 is None:
%		lastNameUnit2 = ""
%	end

%  	dateTimePostedUnix = report["datetime_posted"]
%  	dateTimePosted = datetime.datetime.fromtimestamp(int(dateTimePostedUnix)).strftime('%Y-%m-%d %H:%M:%S')

%	if report["datetime_finished"]:
%  		dateTimeFinishedUnix = report["datetime_finished"]
%  		dateTimeFinished = datetime.datetime.fromtimestamp(int(dateTimeFinishedUnix)).strftime('%Y-%m-%d %H:%M:%S')
%	else:
%		dateTimeFinished = "Not Finished"
%	end

%  	reportHandler = report["handler"]
%  	if reportHandler is None:
%  		reportHandler = "N/A"
%  	end

%  	reportStatus = report["status"]
%  	if reportStatus is None:
%  		reportStatus = "New Report"
%  	end

<div class="container">
	<div class="row-fluid">
		<div class="span3">
			<aside>
				<nav>
					<ul class="nav">
						<li><a href="/dashboard">
							<i class="icon-play"></i> 
							Dashboard</a>
						</li>
						<li class="selected"><a href="/reports">
							<i class="icon-th-list icon-white"></i> 
							Reports</a>
						</li>
						<li><a href="/members">
							<i class="icon-user icon-white"></i> 
							Members</a>
						</li>
					</ul>
				</nav>
			</aside>
		</div>
		<div class="span9" id="content-wrapper">
			<div id="content">

				<!-- Navbar
				================================================== -->
				<section id="stats">
				<header>
					<div class="pull-right">
						<a href="/reports/view/{{id}}" class="btn btn-small btn-primary" target="rid{{id}}">View Report</a>
					</div>
					<h1>Edit Crash Report</h1>
				</header>
				</section>

				<!-- Tables
				================================================== -->
				<section id="tables" style="padding: 30px;">
%if error == 1:
					<div class="alert alert-error">
						There was an error processing your request
					</div>
%end

%if success == 1:
					<div class="alert alert-success">
						Report profile saved successfully
					</div>
%end

					<form action="/reports/edit/submit" method="POST">
					<input type="hidden" name="id" value="{{id}}">
							<label  for="">
								Handler
							</label>
							<select name="handler">
								<option value="">Open</option>
%for handler in handlers:
%	handlerName = "%s %s" % (handler["first_name"], handler["last_name"])
%	if handlerName == reportHandler:
%		selected = "selected=selected"
%	else:
%		selected = ""
%	end					
								<option value="{{handlerName}}" {{selected}}>{{handlerName}}</option>
%end
							</select>

							<label  for="">
								Status
							</label>
							<select name="status">
								<option value="">New Report</option>
%for status in statuses:
%	s = status["status"]
%	if s == reportStatus:
%		selected = "selected=selected"
%	else:
%		selected = ""
%	end					
								<option value="{{s}}" {{selected}}>{{s}}</option>
%end
							</select>

							<label  for="">
								Unit 1 - First Name
							</label>
							<input type="text" name="firstNameUnit1" value="{{firstNameUnit1}}">

							<label  for="">
								Unit 1 - Last Name
							</label>
							<input type="text" name="lastNameUnit1" value="{{lastNameUnit1}}">

							<label  for="">
								Unit 2 - First Name
							</label>
							<input type="text" name="firstNameUnit2" value="{{firstNameUnit2}}">

							<label  for="">
								Unit 2 - Last Name
							</label>
							<input type="text" name="lastNameUnit2" value="{{lastNameUnit2}}">

							<label  for="">
								DateTime Posted
							</label>
							{{dateTimePosted}}<br><br>

							<label  for="">
								DateTime Finished
							</label>
							{{dateTimeFinished}}<br><br>

							<input type="submit" value="Submit Changes" class="btn btn-primary">
					</form>
				</section>
			</div>
		</div>
	</div>
</div><!-- /container -->

% include footer