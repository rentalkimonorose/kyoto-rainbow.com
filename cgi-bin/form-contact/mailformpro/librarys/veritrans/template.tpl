<!DOCTYPE html>
<html lang="ja">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<title>Veritrans</title>
		<style>
			* {
				padding: 0;
				margin: 0;
				box-sizing: border-box;
				font-family: sans-serif;
			}
			body {
				background: #EEE;
				border-top: solid 1px #999;
				padding-bottom: 2em;
			}
			body main {
				border-top: solid 1px #FFF;
				padding: 10px;
			}
			body main form {
				max-width: 480px;
				padding: 30px 15px;
				border-radius: 10px;
				border: solid 1px #CCC;
				margin: 0 auto;
				background: #FFF;
			}
			body main form img {
				display: block;
				margin: 0 auto;
			}
			body main form button {
				display: block;
				margin: 15px auto;
				border-radius: 5px;
				padding: 5px 10px;
				border: solid 1px #CCC;
				background: gradient(linear, center top, center bottom, from(#FEFEFE), to(#DEDEDE));
				background: -webkit-gradient(linear, center top, center bottom, from(#FEFEFE), to(#DEDEDE));
				background: -moz-linear-gradient(top, #FEFEFE, #DEDEDE);
				background: -ms-linear-gradient(top, #FEFEFE 0%, #DEDEDE 100%);
				text-shadow: 0px 2px 0px #FFF;
				font-size: 18px;
				cursor: pointer;
				outline: none;
			}
		</style>
		<script type="text/javascript" src="https://pay.veritrans.co.jp/pop/v1/javascripts/pop.js" data-client-key="_%%clientkey%%_"></script>
	</head>
	<body>
		<main>
_%%main%%_
		<script type="text/javascript">
			window.onload = function(){
				var options = {
				};
				pop.pay("_%%paymentkey%%_", options);
			};
		</script>
		_%%resultcode%%_
		</main>
	</body>
</html>