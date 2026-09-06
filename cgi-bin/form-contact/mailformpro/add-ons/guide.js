// ok.js 1.0.0
// 2014-11-14

mfp.extend.event('init',
	function(obj){
		var ok = 'mfp_guide_' + obj.id;
		if(!mfp.$(ok) && obj.type != 'hidden' && obj.getAttribute('data-guide')){
			var elm = mfp.d.createElement('div');
			elm.className = "mfp_guide";
			var guide = mfp.d.createElement('div');
			guide.innerHTML = obj.getAttribute('data-guide');
			guide.id = ok;
			elm.appendChild(guide);
			obj.parentNode.insertBefore(elm, obj.parentNode.firstChild)
			//obj.parentNode.insertBefore(elm, obj.nextSibling);
			//obj.parentNode.appendChild(elm);
		}
	}
);
mfp.extend.event('focus',
	function(obj){
		var okObj = 'mfp_guide_' + obj.id;
		if(mfp.$(okObj)){
			mfp.$(okObj).style.display = 'block';
		};
	}
);
mfp.extend.event('blur',
	function(obj){
		var okObj = 'mfp_guide_' + obj.id;
		if(mfp.$(okObj)){
			mfp.$(okObj).style.display = 'none';
		};
	}
);
