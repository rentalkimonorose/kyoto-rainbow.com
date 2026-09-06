mfpConfigs['ErrorFocusDisabled'] = true;
mfp.extend.event('elementError',
	function(obj){
		if(mfp.Ready){
			var top = mfp.absolutePosition(obj.id);
			mfp.smoothScroll(top-50,1000);
			setTimeout(function(){
				mfp.$(obj.id).focus();
			},1000);
			//mfp.scroll(obj.id);
		};
	}
);