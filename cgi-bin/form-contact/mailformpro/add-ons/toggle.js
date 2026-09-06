var mfpToggleIds = 0;
var mfpToggleObjects = [];
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-toggle')){
			mfpToggleObjects.push(obj.id);
		};
		if(obj.type == 'select-one'){
			for(var i=0;i<obj.length;i++){
				if(obj.options[i].getAttribute('data-toggle')){
					if(!obj.options[i].id){
						obj.options[i].id = 'mfp_toggle_option_id_' + mfpToggleIds;
						mfpToggleIds++;
					};
					mfpToggleObjects.push(obj.options[i].id);
				};
			};
		};
	}
);
function mfpRemoveToggle(){
	var tObj = mfp.$('mailformpro').getElementsByTagName("input");
	for(var i=0;i<tObj.length;i++){
		tObj[i].removeAttribute('data-toggle-process');
	};
	var tObj = mfp.$('mailformpro').getElementsByTagName("select");
	for(var i=0;i<tObj.length;i++){
		tObj[i].removeAttribute('data-toggle-process');
	};
	var tObj = mfp.$('mailformpro').getElementsByTagName("textarea");
	for(var i=0;i<tObj.length;i++){
		tObj[i].removeAttribute('data-toggle-process');
	};
};
function mfpToggle(){
	mfpRemoveToggle();
	for(var i=mfpToggleObjects.length-1;i>=0;i--){
		var obj = mfp.$(mfpToggleObjects[i]);
		var target = mfp.$(obj.getAttribute('data-toggle'));
		var hide = true;
		var value = obj.getAttribute('data-toggle-value');
		try {
			if(obj.getAttribute('data-toggle-hide')){
				hide = false;
			};
			var block = 'block';
			if(target.tagName == 'SPAN'){
				block = 'inline-block';
			};
			if(!obj.type){
				if(obj.parentNode.value == obj.value){
					mfp.sw(false,obj.getAttribute('data-toggle'),hide,block);
				}
				else {
					mfp.sw(true,obj.getAttribute('data-toggle'),hide,block);
				};
			}
			else if(obj.type == 'checkbox' || obj.type == 'radio'){
				if(obj.checked){
					// show
					mfp.sw(false,obj.getAttribute('data-toggle'),hide,block);
				}
				else {
					// hide
					mfp.sw(true,obj.getAttribute('data-toggle'),hide,block);
				};
			}
			else if(obj.type == 'file'){
				if(obj.value != ''){
					// show
					mfp.sw(false,obj.getAttribute('data-toggle'),hide,block);
				}
				else {
					// hide
					mfp.sw(true,obj.getAttribute('data-toggle'),hide,block);
				};
			}
			else {
				if(obj.value == value){
					// show
					mfp.sw(false,obj.getAttribute('data-toggle'),hide,block);
				}
				else if(obj.value != obj.defaultValue && !value){
					// show
					mfp.sw(false,obj.getAttribute('data-toggle'),hide,block);
				}
				else {
					// hide
					mfp.sw(true,obj.getAttribute('data-toggle'),hide,block);
				};
			};
		}catch(e){console.log(obj);};
	};
};
mfp.extend.event('ready',
	function(obj){
		mfpToggle();
	}
);

mfp.extend.event('blur',
	function(obj){
		mfpToggle();
	}
);

mfp.extend.event('change',
	function(obj){
		mfpToggle();
	}
);
