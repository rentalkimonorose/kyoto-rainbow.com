var googleSpreadSheetConfig = {
	name: 'mfpdata', // シートの名前
	id: '1mdfYAQuHuI0cjt2rmoM4HUiWeCPnN6i6r_FOqsAXBAc', // 共有可能なリンクのid=のあとの文字列
	action: 'https://script.google.com/macros/s/AKfycbx2uq2vr-dvrs9GvfOO7nCu_EdLaMSqbkqNMSUi9tABti4-Fx8/exec', // 現在のウェブアプリケーションのURL
	mailformpro: 'mailformpro/mailformpro.cgi?module=thanks&callback=googleSpreadSheetConnect.callback' // メールフォームプロのURL
};
var googleSpreadSheetConnect = {
	debug: false,
	init: function(){
		var _ = googleSpreadSheetConnect;
		_.ready(function(){
			if(window.top === window.self){
				_.json(googleSpreadSheetConfig['mailformpro']);
			};
		});
	},
	callback: function(json){
		var _ = googleSpreadSheetConnect;
		// set iframe
		var iframe = _.node('iframe');
		iframe.id = 'google_spreadsheet_iframe';
		iframe.name = 'google_spreadsheet_iframe';
		iframe.style.display = 'none';
		document.body.appendChild(iframe);
		
		// set form
		var form = _.node('form');
		form.id = 'google_spreadsheet_form';
		form.action = googleSpreadSheetConfig['action'];
		form.method = 'POST';
		form.target = 'google_spreadsheet_iframe';
		form.style.display = 'none';
		
		json['SPREADSHEET_ID'] = googleSpreadSheetConfig['id'];
		json['SHEET_NAME'] = googleSpreadSheetConfig['name'];
		
		form.appendChild(_.elements(json));
		
		if(_.debug){
			var elm = document.createElement('button');
			elm.type = 'submit';
			elm.innerHTML = 'submit';
			form.appendChild(elm);
			form.target = '_self';
			document.body.appendChild(form);
			document.getElementById('google_spreadsheet_form').style.display = 'block';
		}
		else {
			document.body.appendChild(form);
			setTimeout(function(){
				document.getElementById('google_spreadsheet_form').submit();
			},500);
		};
	},
	elements: function(json){
		var _ = googleSpreadSheetConnect;
		var wrap = _.node('div');
		for(var prop in json){
			wrap.appendChild(_.pram(prop,_.sanitizing(json[prop])));
		};
		return wrap;
	},
	node: function(tagName){
		return document.createElement(tagName);
	},
	pram: function(name,value){
		var _ = googleSpreadSheetConnect;
		var elm = _.node('input');
		if(_.debug){
			elm.type = 'text';
			elm.title = name;
		}
		else {
			elm.type = 'hidden';
		};
		elm.name = name;
		elm.value = value;
		return elm;
	},
	json: function(src){
		var script = document.createElement('script');
		script.async = false;
		script.type = 'text/javascript';
		script.src = src;
		script.charset = 'UTF-8';
		document.body.appendChild(script);
	},
	sanitizing: function(str){
		return str.replace(/<br \/>/g,"\n");
	},
	ready: function(fn){
		if(document.addEventListener){
			document.addEventListener("DOMContentLoaded",fn,false);
		}
		else {
			var IEReady = function(){
				try {
					document.documentElement.doScroll("left");
				}
				catch(e) {
					setTimeout(IEReady,1);
					return;
				};
				fn();
			};
			IEReady();
		};
	}
};
googleSpreadSheetConnect.init();