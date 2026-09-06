////////////////////////
// record.js 1.0.0    //
// 2016-03-07         //
// SYNCK GRAPHICA     //
// www.synck.com      //
////////////////////////
var mfpRec = {
	Label: {
		'record': '入力内容を記録する',
		'record_ok': '記録しました',
		'clear': '記録を消去する',
		'clear_ok': '消去しました',
		'restore': '記録を呼び出す',
		'restore_ok': '呼び出しました'
	},
	Prefix: null,
	Name: [],
	Objects: [],
	init: function(){
		var _ = mfpRec;
		if(!_.Prefix){
			var uri = location.pathname.split('/');
			uri.pop();
			_.Prefix = uri.join('/');
		};
		if(window.localStorage){
			var s = window.localStorage;
			if(!document.getElementById('mfp_recorder_record')){
				var elm = document.createElement('button');
				elm.id = 'mfp_recorder_record';
				elm.type = 'button';
				elm.innerHTML = _.Label['record'];
				mfp.Mfp.appendChild(elm);
			};
			if(!document.getElementById('mfp_recorder_clear')){
				var elm = document.createElement('button');
				elm.id = 'mfp_recorder_clear';
				elm.type = 'button';
				elm.innerHTML = _.Label['clear'];
				mfp.Mfp.appendChild(elm);
			};
			if(!document.getElementById('mfp_recorder_restore')){
				var elm = document.createElement('button');
				elm.id = 'mfp_recorder_restore';
				elm.type = 'button';
				elm.innerHTML = _.Label['restore'];
				mfp.Mfp.insertBefore(elm, mfp.Mfp.firstChild);
			};
			_.display();
			document.getElementById('mfp_recorder_record').onclick = function(){
				mfpRec.record();
			};
			document.getElementById('mfp_recorder_clear').onclick = function(){
				mfpRec.clear();
			};
			document.getElementById('mfp_recorder_restore').onclick = function(){
				mfpRec.restore();
			};
		};
	},
	display: function(delay){
		var interval = delay || 0;
		var _ = mfpRec;
		var s = window.localStorage;
		setTimeout(function(){
			if(!s[_.Prefix]){
				document.getElementById('mfp_recorder_clear').style.display = 'none';
				document.getElementById('mfp_recorder_restore').style.display = 'none';
				if(document.getElementById('mfp_recorder_wrap')){
					document.getElementById('mfp_recorder_wrap').style.display = 'none';
				};
				document.getElementById('mfp_recorder_record').className = '';
			}
			else {
				document.getElementById('mfp_recorder_clear').style.display = 'inline-block';
				document.getElementById('mfp_recorder_restore').style.display = 'inline-block';
				if(document.getElementById('mfp_recorder_wrap')){
					document.getElementById('mfp_recorder_wrap').style.display = 'block';
				};
				document.getElementById('mfp_recorder_record').className = 'enabled';
			};
		},interval);
	},
	record: function(){
		var _ = mfpRec;
		var s = window.localStorage;
		for(var i=0;i<_.Objects.length;i++){
			var n = _.Objects[i].name;
			var e = mfp.Mfp.elements[n];
			var v = [];
			if(e.length && e.type != 'select-one'){
				for(var ii=0;ii<e.length;ii++){
					if(e[ii].checked){
						v.push(e[ii].value);
					};
				};
			}
			else {
				v.push(e.value);
			};
			s[_.Prefix+'_'+n] = v.join("\n");
		};
		s[_.Prefix] = 1;
		_.display();
		document.getElementById('mfp_recorder_record').innerHTML = mfpRec.Label['record_ok'];
		document.getElementById('mfp_recorder_clear').innerHTML = mfpRec.Label['clear'];
		document.getElementById('mfp_recorder_clear').className = '';
		//alert(mfpRec.Label['record_ok']);
	},
	clear: function(){
		var _ = mfpRec;
		var s = window.localStorage;
		for(var prop in s){
			if(prop.match(new RegExp("^"+_.Prefix+'_'))){
				s.removeItem(prop);
			};
		};
		s.removeItem(_.Prefix);
		_.display(1000);
		document.getElementById('mfp_recorder_clear').innerHTML = mfpRec.Label['clear_ok'];
		document.getElementById('mfp_recorder_clear').className = 'enabled';
		document.getElementById('mfp_recorder_record').innerHTML = mfpRec.Label['record'];
		document.getElementById('mfp_recorder_record').className = '';
		document.getElementById('mfp_recorder_restore').className = '';
		document.getElementById('mfp_recorder_restore').innerHTML = mfpRec.Label['restore'];
		//alert(mfpRec.Label['clear_ok']);
	},
	restore: function(){
		var _ = mfpRec;
		var s = window.localStorage;
		for(var i=0;i<_.Objects.length;i++){
			var n = _.Objects[i].name;
			var e = mfp.Mfp.elements[n];
			if(s[_.Prefix+'_'+n]){
				var v = s[_.Prefix+'_'+n];
				if(e.length && e.type != 'select-one'){
					var val = v.split("\n");
					for(var ii=0;ii<e.length;ii++){
						for(var iii=0;iii<val.length;iii++){
							if(e[ii].value == val[iii]){
								e[ii].checked = true;
							};
						};
					};
				}
				else if(e.type == 'checkbox' || e.type == 'radio'){
					if(e.value == v){
						e.checked = true;
					}
				}
				else {
					e.value = v;
				};
				mfp.check(_.Objects[i]);
			};
		};
		document.getElementById('mfp_recorder_restore').className = 'enabled';
		document.getElementById('mfp_recorder_restore').innerHTML = mfpRec.Label['restore_ok'];
	},
	add: function(obj){
		mfpRec.Objects.push(obj);
	}
};
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-record') && !mfpRec.Name[obj.name]){
			mfpRec.add(obj);
		};
	}
);
mfp.extend.event('ready',
	function(obj){
		mfpRec.init();
	}
);