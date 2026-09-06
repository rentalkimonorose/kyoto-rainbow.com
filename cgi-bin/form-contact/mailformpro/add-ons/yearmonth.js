mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-yearmonth')){
			obj.value = '';
			if(!obj.getAttribute('data-yearmonth-show')){
				obj.style.display = 'none';
			}
			else {
				obj.style.display = 'block';
			};
			var pref = obj.getAttribute('data-yearmonth').split(',');
			var min = mfp.Stat.date.getFullYear() - pref[0];
			var max = mfp.Stat.date.getFullYear() - pref[1];
			var selected = parseInt((max - min) / 2);
			
			(function(){
				var select = document.createElement('select');
				select.onchange = function(){
					mfpym.change(this);
				};
				//select.name = 'mfp_YearmonthElement_'+obj.id+'_month';
				select.id = 'mfp_YearmonthElement_'+obj.id+'_month';
				select.setAttribute('data-yearmonth-parent',obj.id);
				var option = document.createElement('option');
				option.text = '月';
				option.value = '';
				option.selected = true;
				select.appendChild(option);
				for(var i=1;i<13;i++){
					var option = document.createElement('option');
					option.text = mfpym.digit(i) + '月';
					option.value = i;
					select.appendChild(option);
				};
				obj.parentNode.insertBefore(select,obj.nextSibling);
			})();
			
			(function(){
				var select = document.createElement('select');
				select.onchange = function(){
					mfpym.change(this);
				};
				//select.name = 'mfp_YearmonthElement_'+obj.id+'_year';
				select.id = 'mfp_YearmonthElement_'+obj.id+'_year';
				select.setAttribute('data-yearmonth-parent',obj.id);
				for(var i=min;i<=max;i++){
					var option = document.createElement('option');
					//option.text = i +'年' + mfpym.convert(i,1);
					option.text = i +'年';
					if(obj.getAttribute('data-yearmonth-select-jc')){
						option.text += mfpym.convert(i,1);
					};
					option.value = i;
					select.appendChild(option);
					if(i == (min+selected)){
						var option = document.createElement('option');
						option.text = '年';
						option.value = '';
						option.selected = true;
						select.appendChild(option);
					};
				};
				obj.parentNode.insertBefore(select,obj.nextSibling);
			})();
		};
	}
);
var mfpym = {
	Language: {
		'month': ['','January','February','March','April','May','June','July','August','September','October','November','December'],
		'month_short': ['','Jan.','Feb.','Mar.','Apr.','May','Jun.','Jul.','Aug.','Sep.','Oct.','Nov.','Dec.']
	},
	change: function(obj,check){
		var parent = obj.getAttribute('data-yearmonth-parent');
		var y = document.getElementById('mfp_YearmonthElement_'+parent+'_year').value;
		var m = document.getElementById('mfp_YearmonthElement_'+parent+'_month').value;
		if(y && m){
			var format = document.getElementById(parent).getAttribute('data-yearmonth-format');
			var value = y+'年' + mfpym.digit(m)+'月';
			if(format){
				format = format.replace('$1',y);
				format = format.replace('$2',m);
				format = format.replace('$3',mfpym.convert(y));
				format = format.replace('$4',mfpym.Language.month[m]);
				format = format.replace('$5',mfpym.Language.month_short[m]);
				value = format;
			};
			mfp.noproblem(mfp.$(parent));
			document.getElementById(parent).value = value;
		}
		else {
			document.getElementById(parent).value = "";
		};
		if(check){
			mfp.check(document.getElementById(parent));
		};
	},
	convert: function(y,s){
		var p = '';
		if(s){
			p = ' / ';
		};
		if(y == 2019){
			return p+'平成31年/令和元年';
		}
		else if(y > 2019){
			return p+'令和' + mfpym.digit(y-2019+1) + '年';
		}
		else if(y == 1989){
			return p+'平成元年';
		}
		else if(y > 1989){
			return p+'平成' + mfpym.digit(y-1989+1) + '年';
		}
		else if(y == 1926){
			return p+'昭和元年';
		}
		else if(y > 1926){
			return p+'昭和' + mfpym.digit(y-1926+1) + '年';
		}
		else if(y == 1912){
			return p+'大正元年';
		}
		else if(y > 1912){
			return p+'大正' + mfpym.digit(y-1912+1) + '年';
		}
		else if(y >= 1873){
			return p+'明治' + mfpym.digit(y-1873+6) + '年';
		}
		else {
			return '';
		};
	},
	digit: function(n){
		if(n < 10) n = '0'+n;
		return n;
	}
};