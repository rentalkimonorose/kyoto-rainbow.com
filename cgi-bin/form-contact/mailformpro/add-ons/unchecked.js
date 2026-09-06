var radioObjects = [];
mfp.extend.event('click',
	function(obj){
		if(obj.type == 'radio'){
			if(radioObjects[obj.id]){
				obj.checked = false;
				radioObjects[obj.id] = null;
				mfp.check(obj);
				mfp.extend.run('blur',obj);
			};
			radioObjects[obj.id] = obj.checked;
		};
	}
);
