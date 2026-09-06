mfp.extend.event('blur',
	function(obj){
		if(obj.id == 'CouponCheck' && obj.value != ''){
			//var s = document.createElement("script");
			//var u = '?';
			//if(mfp.$('mfpjs').src.indexOf('?') > -1) u = '&';
			//s.src = mfp.$('mfpjs').src + u + 'addon=coupon/coupon.js&code=' + encodeURI(obj.value);
			//document.body.appendChild(s);
			mfp.call(mfp.$('mfpjs').src,'addon=coupon/coupon.js&code=' + encodeURI(obj.value));
		}
		else if(obj.id == 'CouponCheck'){
			mfp.$('CouponCheck').removeAttribute('data-error');
			mfp.$('CouponCheck_text').innerHTML = '';
			mfp.$('CouponCheck_text').style.display = 'none';
			mfp.check(mfp.$('CouponCheck'));
		};
	}
);

function callbackCouponCheck(error,text){
	if(error){
		mfp.$('CouponCheck').setAttribute('data-error','1');
		mfp.$('CouponCheck').setAttribute('data-error-text',text);
		mfp.$('CouponCheck_text').innerHTML = '';
		mfp.$('CouponCheck_text').style.display = 'none';
		mfp.check(mfp.$('CouponCheck'));
	}
	else {
		mfp.$('CouponCheck').removeAttribute('data-error');
		mfp.$('CouponCheck_text').innerHTML = text;
		mfp.$('CouponCheck_text').style.display = 'block';
		mfp.check(mfp.$('CouponCheck'));
	};
};