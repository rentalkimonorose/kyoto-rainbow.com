<!DOCTYPE html>
<html lang="ja">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width">
		<link rel="apple-touch-icon" sizes="256x256" href="./librarys/numticket/logo-touch-icon.png">
		<title>_%%title%%_</title>
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
			body header {
				background: gradient(linear, center top, center bottom, from(#FEFEFE), to(#DEDEDE));
				background: -webkit-gradient(linear, center top, center bottom, from(#FEFEFE), to(#DEDEDE));
				background: -moz-linear-gradient(top, #FEFEFE, #DEDEDE);
				background: -ms-linear-gradient(top, #FEFEFE 0%, #DEDEDE 100%);
				border-top: solid 1px #FFF;
				border-bottom: solid 1px #999;
			}
			body header h1 {
				font-size: 18px;
				padding: 0.5em 1em;
				text-align: left;
				text-shadow: 0px 2px 0px #FFF;
			}
			body main {
				border-top: solid 1px #FFF;
				padding: 10px;
			}
			body main div#wrapper {
				max-width: 960px;
				margin: 0 auto;
			}
			body main div#wrapper section {
				margin: 10px auto;
				background: #FFF;
				border: solid 1px #666;
				border-radius: 5px;
				padding: 15px;
			}
			body main div#wrapper section img {
				display: block;
				max-width: 100%;
				margin: 0 auto;
			}
			body main div#wrapper section h2 {
				font-size: 18px;
				color: #666;
				font-weight: normal;
			}
			body main div#wrapper p.right {
				text-align: right;
			}
			body main div#wrapper p.result {
				font-size: 24px;
				text-align: center;
				padding: 30px 0;
			}
			body main div#wrapper table {
				border-spacing: 0px;
				border-collapse: collapse;
				width: 100%;
			}
			body main div#wrapper table.list thead tr th,
			body main div#wrapper table.list thead tr td {
				padding: 5px 0;
			}
			body main div#wrapper table.list thead tr th,
			body main div#wrapper table.list thead tr td,
			body main div#wrapper table.list tbody tr th,
			body main div#wrapper table.list tbody tr td {
				border: solid 1px #CCC;
				font-size: 12px;
				text-align: center;
			}
			body main div#wrapper table.list tbody tr.tr0 {
				background: #FFF;
			}
			body main div#wrapper table.list tbody tr.tr1 {
				background: #F6F7F9;
			}
			body main div#wrapper table.list tbody tr td div {
				padding: 10px 10px 10px 50px;
				text-align: left;
			}
			body main div#wrapper table.list tbody tr td:nth-child(1) {
				width: 50px;
			}
			body main div#wrapper table.list tbody tr th:nth-child(2) {
				text-decoration: underline;
				font-size: 18px;
				user-select: none;
				cursor: pointer;
			}
			body main div#wrapper table.list tbody tr td:nth-child(3),
			body main div#wrapper table.list tbody tr td:nth-child(4),
			body main div#wrapper table.list tbody tr td:nth-child(5),
			body main div#wrapper table.list tbody tr td:nth-child(6) {
				width: 100px;
			}
			body main div#wrapper table.list tbody tr td:nth-child(7),
			body main div#wrapper table.list tbody tr td:nth-child(8),
			body main div#wrapper table.list tbody tr td:nth-child(9) {
				width: 60px;
			}
			body main div#wrapper table.list tbody tr td.line {
				position: relative;
				background-color: #c6c6c6;
			}
			body main div#wrapper table.list tbody tr td.line span {
				position: absolute;
				top: -0.3em;
				right: 0.1em;
				font-size: 10px;
				color: #FFF;
				background: #900;
				border: solid 1px #FFF;
				border-radius: 2px;
				padding: 0 0.3em;
			}
			body main div#wrapper table.list tbody tr td.active {
				background-color: #00b300;
			}
			body main div#wrapper table.list tbody tr td.line button {
				max-width: 100%;
				width: 100%;
				height: 100%;
				display: block;
				border: none;
				background: none;
				cursor: pointer;
			}
			body main div#wrapper table.list tbody tr td.line button div {
				max-width: 30px;
				padding: 0;
				width: 1.5em;
				height: 1.5em;
				margin: 0 auto;
			}
			.line_icon {
				background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjZERDgzRTMzODkwRTExRUE4MDRBRDU4MzM2MzZBQThEIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjZERDgzRTM0ODkwRTExRUE4MDRBRDU4MzM2MzZBQThEIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6NkREODNFMzE4OTBFMTFFQTgwNEFENTgzMzYzNkFBOEQiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6NkREODNFMzI4OTBFMTFFQTgwNEFENTgzMzYzNkFBOEQiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7HujVoAAAHwUlEQVR42uxdD4gVRRj/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);
				background-repeat: no-repeat;
				background-size: 1em 1em;
				background-position: center center;
			}
			
			@media screen and (max-width: 800px) {
				body main div#wrapper table.list thead tr th:nth-child(4),
				body main div#wrapper table.list thead tr th:nth-child(5),
				body main div#wrapper table.list thead tr th:nth-child(6),
				body main div#wrapper table.list tbody tr td:nth-child(4),
				body main div#wrapper table.list tbody tr td:nth-child(5),
				body main div#wrapper table.list tbody tr td:nth-child(6) {
					display: none;
				}
				body main div#wrapper table.list tbody tr td:nth-child(7),
				body main div#wrapper table.list tbody tr td:nth-child(8),
				body main div#wrapper table.list tbody tr td:nth-child(9) {
					width: 50px;
				}
			}
			body main div#wrapper table.ticket thead tr th,
			body main div#wrapper table.ticket thead tr td,
			body main div#wrapper table.ticket tbody tr th,
			body main div#wrapper table.ticket tbody tr td {
				padding: 5px;
				border-top: solid 1px #CCC;
			}
			body main div#wrapper section table.list tbody tr td form button {
				border: none;
				border-radius: 0;
				font-size: 12px;
				max-width: 100px;
			}
			body main div#wrapper table.ticket thead tr th,
			body main div#wrapper table.ticket tbody tr th {
				font-size: 12px;
				font-weight: normal;
				color: #666;
			}
			body main div#wrapper table.ticket thead tr td,
			body main div#wrapper table.ticket tbody tr td {
				font-weight: bolder;
				font-size: 10vw;
			}
			body main div#wrapper table.ticket tbody tr td {
				font-size: 8vw;
			}
			@keyframes onAutoFillStart { from {} to {}}
			input:-webkit-autofill {
				animation-name: onAutoFillStart;
				transition: background-color 50000s ease-in-out 0s;
			}
			body main div#wrapper section form input,
			body main div#wrapper section form select,
			body main div#wrapper section form textarea {
				width: 100%;
				display: block;
				background: #FFF;
				border: solid 1px #CCC;
				border-radius: 3px;
				box-shadow: 0px 0px 5px #CCC inset;
				padding: 3px 8px;
				vertical-align: middle;
				font-size: 16px;
			}
			body main div#wrapper section form button {
				width: 100%;
				display: block;
				border-radius: 5px;
				padding: 5px 10px;
				border: solid 1px #CCC;
				background: gradient(linear, center top, center bottom, from(#FEFEFE), to(#DEDEDE));
				background: -webkit-gradient(linear, center top, center bottom, from(#FEFEFE), to(#DEDEDE));
				background: -moz-linear-gradient(top, #FEFEFE, #DEDEDE);
				background: -ms-linear-gradient(top, #FEFEFE 0%, #DEDEDE 100%);
				text-shadow: 0px 2px 0px #FFF;
				font-size: 16px;
				cursor: pointer;
				outline: none;
			}
			body main div#wrapper section form dl {
				padding: 10px 0;
			}
			body main div#wrapper section form dl dt {
				color: #999;
				font-size: 14px;
			}
			body main div#wrapper section form dl dd {
				padding-bottom: 1em;
			}
			
			body footer {
				position: fixed;
				width: 100%;
				left: 0;
				bottom: 0;
				background: gradient(linear, center top, center bottom, from(#FEFEFE), to(#DEDEDE));
				background: -webkit-gradient(linear, center top, center bottom, from(#FEFEFE), to(#DEDEDE));
				background: -moz-linear-gradient(top, #FEFEFE, #DEDEDE);
				background: -ms-linear-gradient(top, #FEFEFE 0%, #DEDEDE 100%);
				border-top: solid 1px #999;
			}
			body footer p {
				border-top: solid 1px #FFF;
				padding: 0.5em 1em;
				text-align: right;
			}
			body footer p a {
				font-size: 12px;
				color: #666;
				text-decoration: none;
			}
			div#status {
				position: fixed;
				top: 5px;
				right: 5px;
				display: inline-block;
				background: #900;
				color: #FFF;
				font-size: 16px;
				border-radius: 5px;
				padding: 5px 10px;
			}
			form#reload {
				position: fixed;
				right: 10px;
				top: 10px;
				width: 60px;
				height: 60px;
			}
			form#reload button#reload_button {
				width: 50px;
				height: 50px;
				border: none;
				background: none;
				border: solid 3px #FFF;
				padding: 5px;
				outline: none;
				box-shadow: 0px 2px 10px #000;
				background: #090;
				border-radius: 25px;
				cursor: pointer;
			}
			form#reload button#reload_button.update {
				background: #900;
			}
			form#reload button#reload_button img {
				display: block;
				max-width: 100%;
			}
			section.ticket p strong {
				display: block;
				text-align: center;
				color: #900;
				font-size: 62px;
				line-height: 1em;
			}
			section.ticket p.center {
				text-align: center;
				font-size: 16px;
				color: #666;
			}
		</style>
		<script type="text/javascript">
			var numticket = {
				data: {
					update: _%%time%%_000,
					interval: null
				},
				path: {
					list: '_%%json%%_',
					update: '_%%update%%_'
				},
				action: {
					json: function(src){
						src = src + '?' + (new Date()-1);
						var script = document.createElement('script');
						script.async = false;
						script.type = 'text/javascript';
						script.src = src;
						script.charset = 'UTF-8';
						script.onerror = function(){
							numticket.action.json(src);
						};
						document.body.appendChild(script);
					},
					callback: {
						update: function(time){
							time = time * 1000;
							if(time > numticket.data.update){
								if(document.getElementById('reload_button')){
									document.getElementById('reload_button').className = 'update';
								};
								numticket.action.json(numticket.path.list);
							}
							else {
								clearTimeout(numticket.data.interval);
								setTimeout(function(){
									numticket.action.json(numticket.path.update);
								},5000);
							};
						},
						list: function(json){
							console.log(json);
							numticket.data.update = json.time * 1000;
							if(document.getElementById('html_total_index')){
								document.getElementById('html_total_index').innerHTML = json.qty;
							};
							if(document.getElementById('html_total_waitTime')){
								document.getElementById('html_total_waitTime').innerHTML = ((json.qty+1) * json.wait) + '分';
							};
							if(json.message){
								if(document.getElementById('message_wrapper')){
									document.getElementById('message_wrapper').style.display = 'block';
									document.getElementById('message_inner').innerHTML = json.message;
								};
							}
							else {
								if(document.getElementById('message_wrapper')){
									document.getElementById('message_wrapper').style.display = 'none';
								};
							};
							if(document.getElementById('html_next')){
								if(json.qty > 0){
									document.getElementById('html_next_wrapper').style.display = 'block';
									document.getElementById('html_next').innerHTML = json.list[0].num;
								}
								else {
									document.getElementById('html_next_wrapper').style.display = 'none';
								};
							};
							if(document.getElementById('html_numticket')){
								var numticketCode = document.getElementById('html_numticket').innerHTML;
								var index = null;
								for(var i=0;i<json.list.length;i++){
									if(json.list[i].num == numticketCode){
										index = i + 1;
									};
								};
								if(index != null){
									if(document.getElementById('html_index')){
										document.getElementById('html_index').innerHTML = index;
									};
									if(document.getElementById('html_waitTime')){
										document.getElementById('html_waitTime').innerHTML = (index * json.wait) + '分';
									};
								}
								else {
									window.location.reload();
								};
							};
							clearTimeout(numticket.data.interval);
							setTimeout(function(){
								numticket.action.json(numticket.path.update);
							},5000);
						}
					}
				}
			};
			window.onload = function(){
				if(document.getElementById('status')){
					setTimeout(function(){
						document.getElementById('status').style.display = 'none';
					},3000);
				};
				if(document.getElementById('line_message_wrapper')){
					document.getElementById('line_message_wrapper').style.display = 'none';
					var elm = document.body.getElementsByTagName('button');
					for(var i=0;i<elm.length;i++){
						if(elm[i].getAttribute('data-hash')){
							elm[i].onclick = function(){
								document.getElementById('line_message_wrapper').style.display = 'block';
								document.getElementById('line_hash').value = this.getAttribute('data-hash');
								document.getElementById('line_num').value = this.getAttribute('data-num');
								document.getElementById('line_message').focus();
							};
						};
					};
				};
				numticket.data.interval = setTimeout(function(){
					numticket.action.json(numticket.path.update);
				},5000);
			};
			var showObject = [];
			function show(id){
				if(showObject[id]){
					showObject[id] = false;
					document.getElementById(id).style.display = 'none';
				}
				else {
					showObject[id] = true;
					document.getElementById(id).style.display = 'table-row';
				};
			};
		</script>
	</head>
	<body>
		<header>
			<h1>Number Ticket</h1>
		</header>
		<main>
			<div id="wrapper">
				_%%content%%_
			</div>
		</main>
		_%%footer%%_
		_%%status%%_
	</body>
</html>