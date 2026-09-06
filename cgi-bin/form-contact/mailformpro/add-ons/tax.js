//
// tax.js 1.0.1 / 2016-08-26
//

// $1:消費税
mfpConfigs['tax'] = 0.1;
mfpLang['taxName'] = '消費税';
mfpLang['tax'] = '（うち消費税 $1 円）';
mfpLang['taxvalue'] = '$1 円';

function taxCalc(){
	var tax = parseInt(mfp.Price * mfpConfigs['tax']);
	mfp.Price += tax;
	var taxStr = mfp.cm(tax);
	if(mfp.$('mfp_tax_element')){
		mfp.$('mfp_tax_element').value = mfpLang['taxvalue'].replace('$1',taxStr);
		mfp.addcart(mfpLang['taxName'],'tax',tax,1);
	};
	if(mfp.$('mfp_tax')){
		if(tax > 0){
			mfp.$('mfp_tax').innerHTML = mfpLang['tax'].replace('$1',taxStr);
		}
		else {
			mfp.$('mfp_tax').innerHTML = "";
		};
	};
};

mfp.extend.event('calc',
	function(){
		taxCalc();
	}
);
mfp.extend.event('startup',
	function(){
		taxCalc();
	}
);
