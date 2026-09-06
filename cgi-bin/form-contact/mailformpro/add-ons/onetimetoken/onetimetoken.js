//
// onetimetoken.js 1.0.0 / 2019-11-25
//

function callbackOnetimeToken(token){
	mfp.$('mfp_token').value = token;
};
mfp.extend.event('startup',
	function(){
		if(!document.getElementById('mfp_token')){
			var elm = mfp.d.createElement('input');
			elm.type = 'hidden';
			elm.id = 'mfp_token';
			elm.name = 'mfp_token';
			mfp.Mfp.insertBefore(elm,mfp.Mfp.firstChild);
		};
		mfp.call(mfp.$('mfpjs').src,'addon=onetimetoken/onetimetoken.js&callback=callbackOnetimeToken');
	}
);
