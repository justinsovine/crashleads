<!DOCTYPE html>
<html>
<head>
<title>{{headline}} - {{tagline}}</title>
<link rel="icon" type="image/png" href="/img/favicon-pdf.png">
<style>
	h1 {
		font-size: 20px;
		font-family: Arial, Helvetica, sans-serif;
		margin: 0px;
		padding: 0px;
	}

	h2 {
		font-size: 16px;
		font-family: Arial, Helvetica, sans-serif;
		margin: 0px 0px 10px 0px;
		padding: 0px;
	}

	hgroup {
		width: 500px;
		text-align: center;
		margin: 0 auto;
	}
</style>

</head>
<body>

<hgroup>
	<h1>{{headline}}</h1>
	<h2>{{tagline}}</h2>
%if cat:
	<img src="/img/H6A53.jpg">
%end
</hgroup>


</body>
</html>
