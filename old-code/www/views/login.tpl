<!DOCTYPE html>
<html>
<head>
	<title>GrabReports - Login</title>
	<link href="/css/inspiritas.css" rel="stylesheet">
	<link href="/css/override.css" rel="stylesheet">

	<style>
		p {
			margin: 0px;
			padding: 0px;
		}

		label {
			font-weight:  bold;
		}

		.logo {
			margin: 100px auto 0px auto; 
			width: 260px;
			text-align: center;
		}

		.loginForm {
			margin: 10px auto 0px auto; 
			width: 260px;
		}

		.alert {
			text-align: center;
		}
	</style>
</head>
<body>
%if loginfail == 2:
		<div class="alert alert-error">The credentials you entered do not match with our records</div>

%end

%if loginfail == 1:
		<div class="alert alert-error">Please enter both a username and password</div>

%end

	<div class="logo">
		<h2>GrabReports</h2>
	</div>
	<!--
	<div class="loginForm">
		<form action="/login" method="POST">
			<p>
				<label for="username">Username</label>
				<input type="text" name="username" value="" style="width: 250px;">
			</p>
			<p>
				<label for="username">Password</label>
				<input type="password" name="password" value="" style="width: 250px;">
			</p>
			<p>
				<input type="submit" value="Log In" class="btn btn-primary" style="width: 265px;">
			</p>
		</form>
	</div>
	-->	
</body>
</html>