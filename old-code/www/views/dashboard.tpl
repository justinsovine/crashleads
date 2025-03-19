% include header title="Dashboard"

<div class="container">
	<div class="row-fluid">
		<div class="span3">
			<aside>
				<nav>
					<ul class="nav">
						<li class="selected"><a href="/dashboard">
							<i class="icon-play"></i> 
							Dashboard</a>
						</li>
						<li><a href="/reports">
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
					<h1>Dashboard</h1>
				  </header>
				  <div class="row-fluid">
					<div class="span2">
						<div class="kpi">400</div>
						<div><small>Reports Today</small></div>
					</div>
					<div class="span2">
						<div class="kpi">2800</div>
						<div><small>Reports This Week</small></div>
					</div>
					<div class="span2">
						<div class="kpi">84,000</div>
						<div><small>Reports Total</small></div>
					</div>
					<div class="span2">
						<div class="kpi">45,000</div>
						<div><small>Reports Handled</small></div>
					</div>
				  </div>
				</section>
				<!-- Graph
				================================================== -->
				<section id="forms">
					<div class="sub-header">
						<h2>Graphs with Highcharts</h2>
					</div>
					<div class="row-fluid row-fluid-alternate-bg">
						<div class="span12">
							<div id="mainChart"></div>
						</div>
					</div>
				</section>

				<!-- Tables
				================================================== -->
				<section id="tables">
				  <div class="sub-header">
					<h2>Recent Reports (Today)</h2>
				  </div>
				  <table class="table table-striped full-section table-hover">
					<thead>
					<tr>
						<th>Action</th>
						<th>Source</th>
						<th>Reports</th>
						<th>Number Handled</th>
						<th>Percent Complete</th>
					</tr>
					</thead>
					<tbody>
					<tr>
						<td class="primary" style="width: 200px;">
							<a href="" class="btn btn-primary btn-small">
							View Reports</a>&nbsp;
							<a href="" class="btn btn-primary btn-small">
							View Source</a>
						</td>
						<td class="primary">PoliceReports.us (compiled)</td>
						<td>100</td>
						<td>25</td>
						<td>
							<div class="progress progress-mini">
								<div class="bar" style="width: 25%"></div>
							</div>
						</td>
					</tr>
					<tr>
						<td class="primary">
							<a href="" class="btn btn-primary btn-small">
							View Reports</a>&nbsp;
							<a href="" class="btn btn-primary btn-small">
							View Source</a>
						</td>
						<td class="primary">Ohio DPS (compiled)</td>
						<td>100</td>
						<td>50</td>
						<td>
							<div class="progress progress-mini">
								<div class="bar" style="width: 50%"></div>
							</div>
						</td>
					</tr>
					<tr>
						<td class="primary">
							<a href="" class="btn btn-primary btn-small">
							View Reports</a>&nbsp;
							<a href="" class="btn btn-primary btn-small">
							View Source</a>
						</td>
						<td class="primary">Lebanon PD</td>
						<td>100</td>
						<td>75</td>
						<td>
							<div class="progress progress-mini">
								<div class="bar" style="width: 75%"></div>
							</div>
						</td>
					</tr>
					<tr>
						<td class="primary">
							<a href="" class="btn btn-primary btn-small">
							View Reports</a>&nbsp;
							<a href="" class="btn btn-primary btn-small">
							View Source</a>
						</td>
						<td class="primary">Butler Township PD</td>
						<td>100</td>
						<td>100</td>
						<td>
							<div class="progress progress-mini">
								<div class="bar" style="width: 100%"></div>
							</div>
						</td>
					</tr>
					<tr>
						<td class="primary">
							<a href="" class="btn btn-primary btn-small">
							View Reports</a>&nbsp;
							<a href="" class="btn btn-primary btn-small">
							View Source</a>
						</td>
						<td class="primary">Mason PD</td>
						<td>100</td>
						<td>75</td>
						<td>
							<div class="progress progress-mini">
								<div class="bar" style="width: 75%"></div>
							</div>
						</td>
					</tr>
					<tr>
						<td class="primary">
							<a href="" class="btn btn-primary btn-small">
							View Reports</a>&nbsp;
							<a href="" class="btn btn-primary btn-small">
							View Source</a>
						</td>
						<td class="primary">Franklin PD</td>
						<td>100</td>
						<td>50</td>
						<td>
							<div class="progress progress-mini">
								<div class="bar" style="width: 50%"></div>
							</div>
						</td>
					</tr>
					<tr>
						<td class="primary">
							<a href="" class="btn btn-primary btn-small">
							View Reports</a>&nbsp;
							<a href="" class="btn btn-primary btn-small">
							View Source</a>
						</td>
						<td class="primary">Miami TWP PD</td>
						<td>100</td>
						<td>25</td>
						<td>
							<div class="progress progress-mini">
								<div class="bar" style="width: 25%"></div>
							</div>
						</td>
					</tr>
					<tr>
						<td class="primary">
							<a href="" class="btn btn-primary btn-small">
							View Reports</a>&nbsp;
							<a href="" class="btn btn-primary btn-small">
							View Source</a>
						</td>
						<td class="primary">Warren Co PD</td>
						<td>100</td>
						<td>50</td>
						<td>
							<div class="progress progress-mini">
								<div class="bar" style="width: 50%"></div>
							</div>
						</td>
					</tr>
					</tbody>
				  </table>
				</section>
			</div>
		</div>
	</div>
</div><!-- /container -->

% include footer