mfpLang['WarningCode'][14] = 'クレジットカード情報に誤りがあるか、有効ではない可能性があります。再度クレジットカードの情報をご確認ください。';
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-creditcard-exp')){
			var y = (new Date()).getFullYear();
			for(var i=0;i<10;i++){
				var elm = mfp.d.createElement('option');
				elm.text = (y+i)+'年';
				elm.value = y+i;
				obj.appendChild(elm);
			};
		};
	}
);
