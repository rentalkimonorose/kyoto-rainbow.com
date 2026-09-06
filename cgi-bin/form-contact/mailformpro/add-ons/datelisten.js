// datelisten.js 1.0.0
// 2019-05-21

mfpLang['week'] = new Array('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');
mfpLang['week_short'] = new Array('Sun.','Mon.','Tue.','Wed.','Thu.','Fri.','Sat.');
mfpLang['month'] = new Array('','January','February','March','April','May','June','July','August','September','October','November','December');
mfpLang['month_short'] = new Array('Jan.','Feb.','Mar.','Apr.','May','Jun.','Jul.','Aug.','Sep.','Oct.','Nov.','Dec.');
mfpLang['dayOptgroup'] = '$M,$y';
mfpLang['dayText'] = '$y/$m/$d $W';
//mfpLang['dayText'] = '$d日($w)';
mfpLang['dayValue'] = '$y-$m-$d';
mfpConfigs['weekColors'] = new Array('#FEE','#FFF','#FFF','#FFF','#FFF','#FFF','#EEF');

// $y ... 年実数
// $m ... 月実数
// $d ... 日実数
// $w ... 曜日
// $M ... 月英字
// $MS ... 月英字短縮
// $W ... 曜日短縮

// data-daystart="5"
// 5日後から表示

// data-daymax="60"
// 60日間分表示

// data-dayexc="2014-12-24,2015-01-01"
// 2014年12月24日と2015年01月01日は非表示

// data-dayexcon="2014-12-25,2015-01-02"
// 2014年12月25日と2015年01月02日は表示

// data-weekexc="1,0,0,0,0,0,0"
// 日・月・火・水・木・金・土 で非表示は1
// 上記の例では日曜日は非表示

function mfpDayFormatEn(y,m,d,w,str){
	str = str.replace('$y',y);
	str = str.replace('$m',m);
	str = str.replace('$MS',mfpLang['month_short'][parseInt(m)]);
	str = str.replace('$M',mfpLang['month'][parseInt(m)]);
	str = str.replace('$d',d);
	str = str.replace('$w',mfpLang['week'][w]);
	str = str.replace('$W',mfpLang['week_short'][w]);
	return str;
}
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-daystart') && obj.getAttribute('data-daymax')){
			var daymax = Number(obj.getAttribute('data-daymax'));
			var daystart = Number(obj.getAttribute('data-daystart'));
			var lastday = obj.getAttribute('data-lastday');
			var excweek = new Array();
			var excdates = new Array();
			var excday = "";
			var excdayon = "";
			if(obj.getAttribute('data-lastday')){
				lastday = new Date(obj.getAttribute('data-lastday'));
			};
			if(obj.getAttribute('data-weekexc')){
				excweek = obj.getAttribute('data-weekexc').split(',');
			};
			if(obj.getAttribute('data-dayexc')){
				excday = obj.getAttribute('data-dayexc');
			};
			if(obj.getAttribute('data-dayexcon')){
				excdayon = obj.getAttribute('data-dayexcon');
			};
			var daycount = 0;
			var optgroup = "";
			while(daycount < daymax){
				var t = (Number(mfpConfigs['Time']) + ((daystart + daycount) * 86400))  * 1000;
				var dayDate = new Date(t);
				if(!lastday || dayDate.getTime() <= lastday.getTime()){
					var num = obj.length;
					var y = dayDate.getFullYear();
					var m = dayDate.getMonth() + 1;
					var d = dayDate.getDate();
					var w = dayDate.getDay();
					if(m < 10) m = '0'+m;
					if(d < 10) d = '0'+d;
					var daystr = y+"-"+m+"-"+d;
					if(excweek[dayDate.getDay()] == undefined || excweek[dayDate.getDay()] == 0 || excdayon.indexOf(daystr) > -1){
						if(excday.indexOf(daystr) == -1){
							if(navigator.userAgent.indexOf("MSIE") == -1) {
								if(optgroup != (obj.id+'-'+y+'-'+m)){
									var elm = mfp.d.createElement('optgroup');
									elm.label = mfpDayFormatEn(y,m,d,w,mfpLang['dayOptgroup']);
									elm.id = (obj.id+'-'+y+'-'+m);
									obj.appendChild(elm);
									optgroup = (obj.id+'-'+y+'-'+m);
								}
								var elm = mfp.d.createElement('option');
								elm.text = mfpDayFormatEn(y,m,d,w,mfpLang['dayText']);
								elm.value = mfpDayFormatEn(y,m,d,w,mfpLang['dayValue']);
								elm.style.backgroundColor = mfpConfigs['weekColors'][w];
								mfp.$(optgroup).appendChild(elm);
							}
							else {
								obj.length++;
								obj.options[num].text = mfpDayFormatEn(y,m,d,w,mfpLang['dayText']);
								obj.options[num].value = mfpDayFormatEn(y,m,d,w,mfpLang['dayValue']);
								obj.options[num].style.backgroundColor = mfpConfigs['weekColors'][w];
							}
						}
					}
				};
				daycount++;
			}
		}
	}
);
