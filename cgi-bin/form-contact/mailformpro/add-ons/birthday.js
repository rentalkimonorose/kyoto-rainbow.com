mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-birthday')){
			obj.value = '';
			if(!obj.getAttribute('data-birthday-show')){
				obj.style.display = 'none';
			}
			else {
				obj.style.display = 'block';
			};
			var pref = obj.getAttribute('data-birthday').split(',');
			var min = mfp.Stat.date.getFullYear() - pref[0];
			var max = mfp.Stat.date.getFullYear() - pref[1];
			var selected = parseInt((max - min) / 2);
			
			(function(){
				var select = document.createElement('select');
				select.onchange = function(){
					mfpbd.change(this,true);
				};
				//select.name = 'mfp_BirthdayElement_'+obj.id+'_day';
				select.id = 'mfp_BirthdayElement_'+obj.id+'_day';
				select.setAttribute('data-birthday-parent',obj.id);
				var option = document.createElement('option');
				option.text = '日';
				option.value = '';
				option.selected = true;
				select.appendChild(option);
				for(var i=1;i<32;i++){
					var option = document.createElement('option');
					option.text = mfpbd.digit(i) + '日';
					option.value = i;
					select.appendChild(option);
				};
				obj.parentNode.insertBefore(select,obj.nextSibling);
			})();
			
			(function(){
				var select = document.createElement('select');
				select.onchange = function(){
					mfpbd.change(this);
				};
				//select.name = 'mfp_BirthdayElement_'+obj.id+'_month';
				select.id = 'mfp_BirthdayElement_'+obj.id+'_month';
				select.setAttribute('data-birthday-parent',obj.id);
				var option = document.createElement('option');
				option.text = '月';
				option.value = '';
				option.selected = true;
				select.appendChild(option);
				for(var i=1;i<13;i++){
					var option = document.createElement('option');
					option.text = mfpbd.digit(i) + '月';
					option.value = i;
					select.appendChild(option);
				};
				obj.parentNode.insertBefore(select,obj.nextSibling);
			})();
			
			(function(){
				var select = document.createElement('select');
				select.onchange = function(){
					mfpbd.change(this);
				};
				//select.name = 'mfp_BirthdayElement_'+obj.id+'_year';
				select.id = 'mfp_BirthdayElement_'+obj.id+'_year';
				select.setAttribute('data-birthday-parent',obj.id);
				for(var i=min;i<=max;i++){
					var option = document.createElement('option');
					//option.text = i +'年' + mfpbd.convert(i,1);
					option.text = i +'年';
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
var mfpbd = {
	change: function(obj,check){
		var parent = obj.getAttribute('data-birthday-parent');
		var j = document.getElementById(parent).getAttribute('data-birthday-jc');
		var a = document.getElementById(parent).getAttribute('data-birthday-age');
		var t = document.getElementById(parent).getAttribute('data-birthday-age-target');
		var y = document.getElementById('mfp_BirthdayElement_'+parent+'_year').value;
		var m = document.getElementById('mfp_BirthdayElement_'+parent+'_month').value;
		var d = document.getElementById('mfp_BirthdayElement_'+parent+'_day').value;
		if(y && m && d){
			var type = document.getElementById(parent).getAttribute('data-type') || document.getElementById(parent).type;
			mfp.noproblem(mfp.$(parent));
			if(t){
				try {
					mfp.$(t).value = mfpbd.age(y,m,d,true);
				}
				catch(e){
					mfp.$(t).innerHTML = mfpbd.age(y,m,d,true) + '才';
				};
			};
			if(type == 'date'){
				document.getElementById(parent).value = y+'-'+mfpbd.digit(m)+'-'+mfpbd.digit(d);
			}
			else {
				var age = "";
				if(a){
					age = mfpbd.age(y,m,d);
				};
				if(j){
					document.getElementById(parent).value = mfpbd.convert(y) + mfpbd.digit(m)+'月'+mfpbd.digit(d)+'日'+age;
				}
				else {
					document.getElementById(parent).value = y+'年' + mfpbd.digit(m)+'月'+mfpbd.digit(d)+'日'+age;
				};
			};
		}
		else {
			document.getElementById(parent).value = "";
			if(t){
				try {
					mfp.$(t).value = "";
				}
				catch(e){
					mfp.$(t).innerHTML = "";
				};
			};
		};
		if(check){
			mfp.check(document.getElementById(parent));
		};
	},
	age: function(y,m,d,t){
		var age = mfp.Stat.date.getFullYear() - y;
		var date = new Date(mfp.Stat.date.getFullYear()+'/'+m+'/'+d);
		if(date.getTime() > mfp.Stat.date.getTime()){
			age--;
		};
		if(t){
			return age;
		}
		else {
			return '（'+age+'才）';
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
			return p+'令和' + mfpbd.digit(y-2019+1) + '年';
		}
		else if(y == 1989){
			return p+'平成元年';
		}
		else if(y > 1989){
			return p+'平成' + mfpbd.digit(y-1989+1) + '年';
		}
		else if(y == 1926){
			return p+'昭和元年';
		}
		else if(y > 1926){
			return p+'昭和' + mfpbd.digit(y-1926+1) + '年';
		}
		else if(y == 1912){
			return p+'大正元年';
		}
		else if(y > 1912){
			return p+'大正' + mfpbd.digit(y-1912+1) + '年';
		}
		else if(y >= 1873){
			return p+'明治' + mfpbd.digit(y-1873+6) + '年';
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