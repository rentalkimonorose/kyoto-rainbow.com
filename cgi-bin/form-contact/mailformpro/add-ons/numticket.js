mfpLang['numticket'] = [];
mfpLang['numticket']['wait'] = "人が待っています";
mfpLang['numticket']['nowait'] = "待っている人はいません";

mfp.extend.event('ready',
	function(){
		numticket.action.json(mfp.uri('module=numticket&json=1'));
		if(!document.getElementById('mfp_numticket_wrapper')){
			var elm = mfp.d.createElement('div');
			elm.id = 'mfp_numticket_wrapper';
			elm.innerHTML = '<section id="numticket_message_wrapper"><p id="message_inner"></p></section><section id="numticket_waitTime"><p>現在の待ち時間<strong id="html_total_waitTime"></strong></p><p class="numticket_center" id="mfp_numticket_wait_status">（<span id="html_total_index"></span>'+mfpLang['numticket']['wait']+'）</p><p class="numticket_center" id="mfp_numticket_nowait_status">'+mfpLang['numticket']['nowait']+'</p></section>';
			mfp.Mfp.parentNode.insertBefore(elm, mfp.Mfp)
		};
	}
);
var numticket = {
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
		traffic: function(week,hour){
			var mfpTrafficStatDate = new Date();
			var weekLabel = new Array('日','月','火','水','木','金','土');
			if(week){
				var weekMax = week.slice();
				weekMax.sort(function(a, b) {
					return a - b;
				});
				var max = weekMax[weekMax.length-1];
				var min = max;
				var weekQty = 0;
				for(var i=0;i<7;i++){
					if(week[i] > 0){
						weekQty++;
						if(week[i] < min){
							min = week[i];
						};
					};
				};
				var maxPar = (max / min * 100) - 100;
				var table = document.createElement('table');
				var trBar = document.createElement('tr');
				var trLabel = document.createElement('tr');
				var width = parseInt(100 / weekQty);
				for(var i=0;i<7;i++){
					if(week[i] > 0){
						var thLabel = document.createElement('th');
						thLabel.innerHTML = weekLabel[i];
						trLabel.appendChild(thLabel);
						var tdBar = document.createElement('td');
						tdBar.style.width = width+'%';
						tdBar.vAlign = 'bottom';
						var span = document.createElement('span');
						if(mfpTrafficStatDate.getDay() == i){
							span.className = 'mfp_traffic_status_current';
						};
						//var point = week[i] - (min - 1);
						var point = max / week[i] * 100 - 100;
						if(point > 0){
							point = parseInt(point / maxPar * 100);
						};
						span.style.height = point + '%';
						tdBar.appendChild(span);
						trBar.appendChild(tdBar);
					};
				};
				table.appendChild(trBar);
				table.appendChild(trLabel);
				if(mfp.$('mfp_traffic_status_week')){
					mfp.$('mfp_traffic_status_week').appendChild(table);
				}
				else {
					var div = document.createElement('div');
					var h3 = document.createElement('h3');
					h3.innerHTML = '曜日別混雑状況';
					div.appendChild(h3);
					div.id = 'mfp_traffic_status_week';
					div.className = 'mfp_traffic_status';
					div.appendChild(table);
					mfp.Mfp.parentNode.insertBefore(div, mfp.Mfp)
				};
			};
			if(hour){
				var hourMax = hour.slice();
				hourMax.sort(function(a, b) {
					return a - b;
				});
				var max = hourMax[hourMax.length-1];
				var min = max;
				var hourQty = 0;
				for(var i=0;i<24;i++){
					if(hour[i] > 0){
						hourQty++;
						if(hour[i] < min){
							min = hour[i];
						};
					};
				};
				var maxPar = (max / min * 100) - 100;
				var table = document.createElement('table');
				var trBar = document.createElement('tr');
				var trLabel = document.createElement('tr');
				var width = parseInt(100 / hourQty);
				for(var i=0;i<24;i++){
					if(hour[i] > 0){
						var thLabel = document.createElement('th');
						thLabel.innerHTML = i + '時';
						trLabel.appendChild(thLabel);
						var tdBar = document.createElement('td');
						tdBar.style.width = width+'%';
						tdBar.vAlign = 'bottom';
						var span = document.createElement('span');
						if(mfpTrafficStatDate.getHours() == i){
							span.className = 'mfp_traffic_status_current';
						};
						// var point = hour[i] - (min - 1);
						var point = max / hour[i] * 100 - 100;
						if(point > 0){
							point = parseInt(point / maxPar * 100);
						};
						span.style.height = point + '%';
						tdBar.appendChild(span);
						trBar.appendChild(tdBar);
					};
				};
				table.appendChild(trBar);
				table.appendChild(trLabel);
				if(mfp.$('mfp_traffic_status_hour')){
					mfp.$('mfp_traffic_status_hour').appendChild(table);
				}
				else {
					var div = document.createElement('div');
					var h3 = document.createElement('h3');
					h3.innerHTML = '時間帯別混雑状況（' + weekLabel[mfpTrafficStatDate.getDay()] + '曜日）';
					div.appendChild(h3);
					div.id = 'mfp_traffic_status_hour';
					div.className = 'mfp_traffic_status';
					div.appendChild(table);
					mfp.Mfp.parentNode.insertBefore(div, mfp.Mfp)
				};
			};
		},
		callback: {
			list: function(json){
				if(json.status){
					mfp.Mfp.style.display = 'block';
					if(mfp.$('numticket_waitTime')){
						mfp.$('numticket_waitTime').style.display = 'block';
					};
					if(document.getElementById('html_total_waitTime')){
						document.getElementById('html_total_waitTime').innerHTML = ((json.qty+1) * json.wait) + '分';
					};
					if(document.getElementById('html_total_index')){
						document.getElementById('html_total_index').innerHTML = json.qty;
					};
					if(json.qty > 0){
						mfp.$('mfp_numticket_wait_status').style.display = 'block';
						mfp.$('mfp_numticket_nowait_status').style.display = 'none';
					}
					else {
						mfp.$('mfp_numticket_wait_status').style.display = 'none';
						mfp.$('mfp_numticket_nowait_status').style.display = 'block';
					};
				}
				else {
					mfp.Mfp.style.display = 'none';
					if(mfp.$('numticket_waitTime')){
						mfp.$('numticket_waitTime').style.display = 'none';
					};
				};
				if(mfp.$('numticket_message_wrapper')){
					if(json.message){
						mfp.$('message_inner').innerHTML = json.message;
						mfp.$('numticket_message_wrapper').style.display = 'block';
					}
					else {
						mfp.$('numticket_message_wrapper').style.display = 'none';
					};
				};
				if(json.week || json.hour){
					numticket.action.json(mfp.uri('module=numticket&json=1&traffic=1'));
				};
			}
		}
	}
};