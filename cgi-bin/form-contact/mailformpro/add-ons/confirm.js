mfp.extend.event('check',
	function(obj){
		if(obj.getAttribute('data-confirm') && obj.value != obj.defaultValue && obj.value != ""){
			var name = obj.getAttribute('data-confirm');
			if(mfp.$(mfp.Elements[obj.getAttribute('data-confirm')].group[0]).value != obj.value){
				mfp.ExtendErrorMsg = obj.getAttribute('data-confirm') + 'と $name が一致しません。';
			}
		}
	}
);
