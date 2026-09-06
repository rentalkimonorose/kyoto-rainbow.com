//
// cart.js 1.0.0 / 2013-02-18
//

mfpLang['cart'] = new Array();
mfpLang['cart']['cart'] = 'ご注文商品';
mfpLang['cart']['del'] = '削除';
mfpLang['cart']['notfound'] = '<p>カートに商品が入っていません</p>';
mfpLang['cart']['h1'] = '商品名(単価)';
mfpLang['cart']['h2'] = '数量';
mfpLang['cart']['h3'] = '小計';
mfpLang['cart']['price'] = '$1 円';

// $1:商品名 / $2:ID / $3:数量 / $4:単価 / $5:小計
mfpLang['cart']['format'] = '$1($2) $4円 x $3  $5円';


mfp.Vc = new Object();
function rebuildCart(){
	var cartHTML = "";
	var cartValue = "";
	var renderHTML = "";
	var totalCost = 0
	if(mfp.Vc.length > 0){
		for(var i=0;i<mfp.Vc.length;i++){
			var subtotal = Number(mfp.Vc[i]['price']) * Number(mfp.Vc[i]['qty']);
			var className = 'mfp_colored';
			if(i % 2 == 0) className = 'mfp_achroma';
			cartHTML += '<tr class="'+className+'"><th>'+mfp.Vc[i]['name']+'<span>( '+mfp.Vc[i]['id']+' / '+mfpStr(mfp.cm(mfp.Vc[i]['price']))+' )</span></th><td><select onchange="updateCart(this,'+i+')">'+createOption(mfp.Vc[i]['qty'])+'</select></td></td><td class="msc_price">'+mfpStr(mfp.cm(subtotal))+'</td></tr>';
			if(mfpLang['cart']['format']){
				var itemline = mfpLang['cart']['format'];
				itemline = itemline.replace('$1',mfp.Vc[i]['name']);
				itemline = itemline.replace('$2',mfp.Vc[i]['id']);
				itemline = itemline.replace('$3',mfp.Vc[i]['qty']);
				itemline = itemline.replace('$4',mfp.cm(mfp.Vc[i]['price']));
				itemline = itemline.replace('$5',mfp.cm(subtotal));
				cartValue += itemline + "\n";
			}
			else {
				cartValue += mfp.Vc[i]['name'] + ' x '+ mfp.Vc[i]['qty'] + "\n";
			}
			totalCost += subtotal;
		}
		renderHTML = '<table class="mfp_shoppingcart">';
		
		renderHTML += '<thead>';
		renderHTML += '<tr>';
		renderHTML += '<td colspan="2">'+mfpLang['cart']['h1']+'</td>';
		renderHTML += '<td>'+mfpLang['cart']['h2']+'</td>';
		renderHTML += '<td>'+mfpLang['cart']['h3']+'</td>';
		renderHTML += '</tr>';
		renderHTML += '</thead>';
		
		renderHTML += '<tbody>' + cartHTML + '</tbody>';
		
		renderHTML += '<tfoot>';
		renderHTML += '<tr>';
		renderHTML += '<td colspan="2">&nbsp;</td>';
		renderHTML += '<td>&nbsp;</td>';
		renderHTML += '<td class="msc_price">'+mfpStr(mfp.cm(totalCost))+'</td>';
		renderHTML += '</tr>';
		renderHTML += '</tfoot>';
		
		renderHTML += '</table>';
	}
	else {
		renderHTML = mfpLang['cart']['notfound'];
	}
	mfp.$('mfp_shopping_cart_value').value = cartValue;
	mfp.$('mfp_shopping_cart').innerHTML = renderHTML;
	mfp.calc();
}
function mfpStr(str){
	return mfpLang['cart']['price'].replace('$1',str);
}
function getCart(arr){
	mfp.Vc = arr;
	rebuildCart();
}
function updateCart(obj,num){
	var id = mfp.Vc[num]['id'];
	var qty = obj.value;
	mfp.call(mfp.$('mfpjs').src,'addon=cart/cart.js&update=' + id + '&qty=' + qty + '&callback=getCart');
}
function createOption(num){
	var optionHTML = '<option value="0">'+mfpLang['cart']['del']+'</option>';
	num = Number(num);
	var no = Number(num) - 10;
	if(no < 1) no = 1;
	for(var i=no;i<(num+10);i++){
		if(num == i)
			optionHTML += '<option value="'+i+'" selected="selected">'+i+'</option>';
		else
			optionHTML += '<option value="'+i+'">'+i+'</option>';
	}
	return optionHTML;
}

mfp.extend.event('calc',
	function(){
		for(var i=0;i<mfp.Vc.length;i++){
			mfp.addcart(mfp.Vc[i]['name'],mfp.Vc[i]['id'],mfp.Vc[i]['price'],mfp.Vc[i]['qty']);
			mfp.Price += (Number(mfp.Vc[i]['price']) * Number(mfp.Vc[i]['qty']));
		};
	}
);
mfp.extend.event('startup',
	function(){
		if(!mfp.$('shopping_cart_value'))
			mfp.addhiddenObject('shopping_cart_value','',mfpLang['cart']['cart']);
		if(!document.getElementById('mfp_shopping_cart')){
			var elm = mfp.d.createElement('div');
			elm.id = 'mfp_shopping_cart';
			elm.innerHTML = "Shopping Cart";
			mfp.Mfp.insertBefore(elm,mfp.Mfp.firstChild);
		}
		if(mfp.GET['item']) // add cart
			mfp.call(mfp.$('mfpjs').src,'addon=cart/cart.js&item=' + mfp.GET['item'] + '&qty=' + mfp.GET['qty'] + '&price=' + mfp.GET['price'] + '&name=' + mfp.GET['name'] + '&callback=getCart');
		else // call cart
			mfp.call(mfp.$('mfpjs').src,'addon=cart/cart.js&callback=getCart');
	}
);
mfp.extend.event('check',
	function(obj){
		if(obj.name == 'ご注文商品' && obj.value == ""){
			mfp.ExtendErrorMsg = 'ショッピングカートに商品が登録されていません';
		}
	}
);
