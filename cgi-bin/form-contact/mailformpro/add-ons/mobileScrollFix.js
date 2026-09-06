// 親オブジェクトにposition relativeがかかっている場合、うまく動かなかも
mfp.extend.event('elementError',
	function(obj){
		if(mfp.Ready){
			var ua = navigator.userAgent;
			if(ua.indexOf('Mobile') > -1){
				mfp.scroll(obj.id);
			};
		};
	}
);