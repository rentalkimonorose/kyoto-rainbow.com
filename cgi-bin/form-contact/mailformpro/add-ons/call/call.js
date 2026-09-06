// コール機能
// call.js 1.0.0 / 2019-05-21
var mfpCallToken = null;
var mfpCallBefoeToken = null;
var mfpCallJson = null;
var mfpCallPage = 10;
var mfpCallCurrentPage = 0;
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-call')){
			if(obj.getAttribute('data-call-feedback-price-string')){
				mfp.$(obj.getAttribute('data-call-feedback-price-string')).style.display = 'none';
			};
			mfp.add(obj,"keyup",function(){
				clearTimeout(mfpCallToken);
				if(obj.value != "" && obj.value != mfpCallBefoeToken){
					mfpCallToken = setTimeout(function(){
						var CallBackElements = obj.id;
						var s = document.createElement("script");
						var u = '?';
						if(mfp.$('mfpjs').src.indexOf('?') > -1){
							u = '&';
						};
						if(!CallBackElements[3]){
							CallBackElements[3] = obj.name;
						};
						s.src = mfp.$('mfpjs').src + u + 'addon=call/call.js&q=' + encodeURIComponent(obj.value) + '&id=' + encodeURI(CallBackElements) + '&db=' + obj.getAttribute('data-call');
						mfpCallBefoeToken = obj.value;
						document.body.appendChild(s);
					},500);
				}
				else if(obj.value == ''){
					mfpCallBefoeToken = obj.value;
					mfpCallCallbackUnmatch(obj.id);
				};
			});
		};
	}
);
mfp.extend.event('calc',
	function(){
		var items = mfp.byClassName(document.body,'data-call-item');
		for(var i=0;i<items.length;i++){
			var obj = items[i];
			mfp.addcart(obj.getAttribute('data-call-name'),obj.getAttribute('data-call-id'),obj.getAttribute('data-call-price'),obj.value);
			mfp.Price += (Number(obj.value) * Number(obj.getAttribute('data-call-price')));
		};
	}
);
function mfpCallCallbackError(){
	alert("コール機能の設定が有効ではありません");
};
function mfpCallCallback(json){
	var obj = mfp.$(json['target']);
	obj.value = json['id'];
	mfp.$(obj.getAttribute('data-call-feedback-name')).value = json['name'];
	mfp.$(obj.getAttribute('data-call-feedback-price')).setAttribute('data-call-id',json['id']);
	mfp.$(obj.getAttribute('data-call-feedback-price')).setAttribute('data-call-name',json['name']);
	mfp.$(obj.getAttribute('data-call-feedback-price')).setAttribute('data-call-price',json['price']);
	if(obj.getAttribute('data-call-feedback-price-string')){
		mfp.$(obj.getAttribute('data-call-feedback-price-string')).innerHTML = mfp.cm(json['price']) + '円';
		mfp.$(obj.getAttribute('data-call-feedback-price-string')).style.display = 'block';
	};
	if(obj.getAttribute('data-call-feedback-price-value')){
		mfp.$(obj.getAttribute('data-call-feedback-price-value')).value = mfp.cm(json['price']) + '円';
	};
	mfp.addClassName(mfp.$(obj.getAttribute('data-call-feedback-price')),'data-call-item');
	mfp.calc();
};
function mfpCallCallbackUnmatch(id){
	var obj = mfp.$(id);
	mfp.$(obj.getAttribute('data-call-feedback-name')).value = "";
	mfp.$(obj.getAttribute('data-call-feedback-price')).removeAttribute('data-call-id');
	mfp.$(obj.getAttribute('data-call-feedback-price')).removeAttribute('data-call-name');
	mfp.$(obj.getAttribute('data-call-feedback-price')).removeAttribute('data-call-price');
	if(obj.getAttribute('data-call-feedback-price-string')){
		mfp.$(obj.getAttribute('data-call-feedback-price-string')).innerHTML = "";
		mfp.$(obj.getAttribute('data-call-feedback-price-string')).style.display = 'none';
	};
	if(obj.getAttribute('data-call-feedback-price-value')){
		mfp.$(obj.getAttribute('data-call-feedback-price-value')).value = "";
	};
	mfp.removeClassName(mfp.$(obj.getAttribute('data-call-feedback-price')),'data-call-item');
	mfp.calc();
};