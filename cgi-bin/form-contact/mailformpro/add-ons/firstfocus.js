mfp.extend.event('ready',
	function(obj){
		for(var i=0;i<mfp.Mfp.length;i++){
			if(mfp.Mfp[i].type == 'text'){
				mfp.Mfp[i].focus();
				break;
			}
		};
	}
);
