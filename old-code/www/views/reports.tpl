% include header title="Crash Reports"

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
                    <div class="pull-right" style="display: none">
                        <a class="btn btn-small">Edit</a>
                        <a class="btn btn-small">Shoot me</a>
                    </div>
                    <h1>Crash Reports</h1>
                  </header>
                  <div class="row-fluid">
                    <div class="span9">
                        <form action="/reports/search" method="POST" class="form-inline">
                            <input type="text" class="input-small" placeholder="First Name" name="firstName">
                            <input type="text" class="input-small" placeholder="Last Name" name="lastName">
                            <input type="submit" class="btn btn-primary" value="Search Reports">
                        </form>
                    </div>
                  </div>
                </section>

                <section id="tables">
                  <div class="sub-header">
                    <h2>Reports in Progress</h2>
                  </div>
                  <table class="table table-striped full-section table-hover">
                    <thead>
                    <tr>
                        <th>Action</th>
                        <th>Status</th>
                        <th>Handler</th>
                        <th>Unit 1</th>
                        <th>Unit 2</th>
                        <th>Locale</th>
                        <th>DateTime Posted</th>
                    </tr>
                    </thead>
                    <tbody>
%for report in currentReports:

%   dateTimePostedUnix = report["datetime_posted"]
%   dateTimePosted = datetime.datetime.fromtimestamp(int(dateTimePostedUnix)).strftime('%Y-%m-%d %H:%M:%S')

%   status = report["status"]
%   if status is None or status == "":
%       status = "New Report"
%   end

%   handler = report["handler"]
%   if handler is None or handler == "":
%       handler = "Open"
%   end

%   if report["first_name"] is None or report["last_name"] is None or report["first_name"] == "" or report["last_name"] == "":
%       unit1 = "Not Entered"
%   else:
%       unit1 = "%s %s" % (report["first_name"], report["last_name"])
%   end

%   if report["first_name_2"] is None or report["last_name_2"] is None or report["first_name_2"] == "" or report["last_name_2"] == "":
%       unit2 = "Not Entered"
%   else:
%       unit2 = "%s %s" % (report["first_name_2"], report["last_name_2"])
%   end

%   locale = report["location"]
                    <tr>
                        <td>
                            <a href="/reports/edit/{{report["id"]}}" class="btn btn-primary btn-small" style="width: 25px;">
                            Edit</a>&nbsp;
                            <a href="{{report["local_link"]}}" class="btn btn-primary btn-small" target="rid{{id}}" style="width: 25px;">
                            View</a>
                        </td>
                        <td>
                            {{status}}
                        </td>
                        <td>
                            {{handler}}
                        </td>
                        <td>
                            {{unit1}}
                        </td>
                        <td>
                            {{unit2}}
                        </td>
                        <td>
                            {{locale}}
                        </td>
                        <td>
                            {{dateTimePosted}}
                        </td>
                    </tr>
%end
                    </tbody>
                  </table>
                </section>

                <div style="margin-bottom: 10px;"></div>

                <section id="tables">
                  <div class="sub-header">
                    <h2>New Reports</h2>
                  </div>
                  <table class="table table-striped full-section table-hover">
                    <thead>
                    <tr>
                        <th>Action</th>
                        <th>Status</th>
                        <th>Handler</th>
                        <th>Unit 1</th>
                        <th>Unit 2</th>
                        <th>Locale</th>
                        <th>DateTime Posted</th>
                    </tr>
                    </thead>
                    <tbody>
%for report in reports:

%   dateTimePostedUnix = report["datetime_posted"]
%   dateTimePosted = datetime.datetime.fromtimestamp(int(dateTimePostedUnix)).strftime('%Y-%m-%d %H:%M:%S')

%   status = report["status"]
%   if status is None or status == "":
%       status = "New Report"
%   end

%   handler = report["handler"]
%   if handler is None or handler == "":
%       handler = "Open"
%   end

%   if report["first_name"] is None or report["last_name"] is None or report["first_name"] == "" or report["last_name"] == "":
%       unit1 = "Not Entered"
%   else:
%       unit1 = "%s %s" % (report["first_name"], report["last_name"])
%   end

%   if report["first_name_2"] is None or report["last_name_2"] is None or report["first_name_2"] == "" or report["last_name_2"] == "":
%       unit2 = "Not Entered"
%   else:
%       unit2 = "%s %s" % (report["first_name_2"], report["last_name_2"])
%   end

%   locale = report["location"]
                    <tr>
                        <td>
                            <a href="/reports/edit/{{report["id"]}}" class="btn btn-primary btn-small" style="width: 25px;">
                            Edit</a>&nbsp;
                            <a href="{{report["local_link"]}}" class="btn btn-primary btn-small" target="rid{{id}}" style="width: 25px;">
                            View</a>
                        </td>
                        <td>
                            {{status}}
                        </td>
                        <td>
                            {{handler}}
                        </td>
                        <td>
                            {{unit1}}
                        </td>
                        <td>
                            {{unit2}}
                        </td>
                        <td>
                            {{locale}}
                        </td>
                        <td>
                            {{dateTimePosted}}
                        </td>
                    </tr>
%end
                    </tbody>
                  </table>
                </section>
            </div>
        </div>
    </div>
</div><!-- /container -->

% include footer