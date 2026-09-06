var paypalWebPaymentPlus = {
	Debug: false, // 本番稼働時はfalseにしてください
	Mailformpro: 'mailformpro/mailformpro.cgi?module=thanks&callback=paypalWebPaymentPlus.callback',
	Request: 'https://securepayments.sandbox.paypal.com/acquiringweb',
	ButtonLabel: 'Paypalで決済する',
	Elements: [
		{
			enabled: true,
			name: 'business', // セキュアなマーチャントID
			value: 'EFZDEL6UUKH7Y'
		},
		{
			enabled: true,
			name: 'cmd',
			value: '_hosted-payment'
		},
		{
			enabled: true,
			name: 'return', // 戻り先URL
			value: 'https://www.paypal.jp/'
		},
		{
			enabled: true,
			name: 'buyer_email', // 買い手のメールアドレス
			formElementName: 'email',
			required: false
		},
		{
			enabled: true,
			name: 'subtotal', // 取引の金額
			formElementName: 'お支払い金額',
			required: false,
			number: true
		},
		{
			enabled: false,
			name: 'handling', // 取り扱い手数料。この金額は合計金額のsubtotalに加算されます。
			value: 0
		},
		{
			enabled: true,
			name: 'currency_code', // 支払いの通貨
			value: 'JPY'
		},
		{
			enabled: true,
			name: 'paymentaction',
			value: 'sale'
		},
		{
			enabled: true,
			name: 'invoice', // マーチャントの注文/請求システムの注文番号
			formElementName: 'mfp_serial'
		},
		{
			enabled: true,
			name: 'lc', // ログインページまたはサインアップページの表示言語
			value: 'JP'
		},
		{
			enabled: true,
			name: 'billing_last_name', // 請求先個人の姓
			formElementName: '姓',
			required: false
		},
		{
			enabled: true,
			name: 'billing_first_name', // 請求先個人の名
			formElementName: '名',
			required: false
		},
		{
			enabled: true,
			name: 'night_phone_a', // 米国外の電話番号の国コード
			value: '81'
		},
		{
			enabled: true,
			name: 'night_phone_b', // 米国外の電話番号の国コードを除く全番号
			formElementName: '電話番号',
			required: false
		},
		{
			enabled: true,
			name: 'billing_country', // 請求先住所の国名
			value: 'JP'
		},
		{
			enabled: true,
			name: 'billing_zip', // 請求先住所の郵便番号
			formElementName: '郵便番号',
			required: false
		},
		{
			enabled: true,
			name: 'billing_state', // 請求先住所の都道府県
			formElementName: '都道府県',
			required: false
		},
		{
			enabled: true,
			name: 'billing_city', // 請求先住所の市区町村
			formElementName: '市区町村',
			required: false
		},
		{
			enabled: true,
			name: 'billing_address1', // 請求先住所の番地1
			formElementName: '丁目番地',
			required: false
		},
		{
			enabled: true,
			name: 'billing_address2', // 請求先住所の番地2
			formElementName: '建物名等',
			required: false
		},
		{
			enabled: true,
			name: 'last_name', // 商品の配送先個人の姓
			formElementName: '姓',
			required: false
		},
		{
			enabled: true,
			name: 'first_name', // 商品の配送先個人の名
			formElementName: '名',
			required: false
		},
		{
			enabled: true,
			name: 'country', // 配送先住所の国名
			value: 'JP'
		},
		{
			enabled: true,
			name: 'zip', // 配送先住所の郵便番号
			formElementName: '郵便番号',
			required: false
		},
		{
			enabled: true,
			name: 'state', // 配送先住所の都道府県
			formElementName: '都道府県',
			required: false
		},
		{
			enabled: true,
			name: 'city', // 配送先住所の市区町村
			formElementName: '市区町村',
			required: false
		},
		{
			enabled: true,
			name: 'address1', // 配送先住所の番地1
			formElementName: '丁目番地',
			required: false
		},
		{
			enabled: true,
			name: 'address2', // 配送先住所の番地2
			formElementName: '建物名等',
			required: false
		}
	],
	initialize: function(){
		var _ = paypalWebPaymentPlus;
		_.ready(function(){
			_.json(_.Mailformpro);
		});
	},
	callback: function(json){
		var _ = paypalWebPaymentPlus;
		
		// set form
		var form = _.node('form');
		form.id = 'paypalWebPaymentPlusForm';
		form.action = _.Request;
		form.method = 'POST';
		
		for(var i=0;i<_.Elements.length;i++){
			if(_.Elements[i].enabled){
				var name = _.Elements[i].name;
				var value = json[_.Elements[i].formElementName] || _.Elements[i].value;
				if(_.Elements[i].number){
					value = _.number(value);
				};
				if(value){
					form.appendChild(_.pram(name,value));
				};
			};
		};
		if(document.getElementById('paypalWebPaymentPlusFormWrapper')){
			var elm = document.createElement('button');
			elm.type = 'submit';
			elm.innerHTML = _.ButtonLabel;
			form.appendChild(elm);
			document.getElementById('paypalWebPaymentPlusFormWrapper').appendChild(form);
			document.getElementById('paypalWebPaymentPlusForm').style.display = 'block';
		};
	},
	json: function(src){
		var script = document.createElement('script');
		script.async = false;
		script.type = 'text/javascript';
		script.src = src;
		script.charset = 'UTF-8';
		document.body.appendChild(script);
	},
	elements: function(json){
		var _ = paypalWebPaymentPlus;
		var wrap = _.node('div');
		for(var prop in json){
			wrap.appendChild(_.pram(prop,_.sanitizing(json[prop])));
		};
		return wrap;
	},
	node: function(tagName){
		return document.createElement(tagName);
	},
	pram: function(name,value){
		var _ = paypalWebPaymentPlus;
		var elm = _.node('input');
		if(_.Debug){
			elm.type = 'text';
			elm.title = name;
		}
		else {
			elm.type = 'hidden';
		};
		elm.name = name;
		elm.value = value;
		return elm;
	},
	sanitizing: function(str){
		return str.replace(/<br \/>/g,"\n");
	},
	number: function(str){
		str = str.replace(/<br \/>/g,"");
		str = str.replace(/\,/g,"");
		str = str.replace(/円/g,"");
		str = str.replace(/ /g,"");
		str = str.replace(/&#x2c;/g,"");
		return str;
	},
	ready: function(fn){
		if(document.addEventListener){
			document.addEventListener("DOMContentLoaded",fn,false);
		}
		else {
			var IEReady = function(){
				try {
					document.documentElement.doScroll("left");
				}
				catch(e) {
					setTimeout(IEReady,1);
					return;
				};
				fn();
			};
			IEReady();
		};
	}
};
paypalWebPaymentPlus.initialize();