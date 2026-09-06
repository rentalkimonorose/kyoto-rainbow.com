//
// request.js 1.0.0 / 2016-09-12
//

mfpLang['request'] = [];
mfpLang['request']['cart'] = 'ご依頼資料';
mfpLang['request']['del'] = '取り消し';
mfpLang['request']['h1'] = '名称';
mfpLang['request']['h2'] = '取り消し';

// $1:ID / $2:名称
mfpLang['request']['format'] = '[ $1 ] $2';

var requestObject = {
	List: [],
	rebuild: function(){
		var _ = requestObject;
		if(_.List.length > 0){
			var html = '';
			var value = '';
			for(var i=0;i<_.List.length;i++){
				var className = 'mfp_colored';
				if(i % 2 == 0){
					className = 'mfp_achroma';
				};
				var img = '&nbsp;';
				if(_.List[i]['image']){
					img = '<img src="images/'+_.List[i]['id']+'.png">';
				};
				html += '<tr class="'+className+'">';
				html += '<td class="request_image">'+img+'</td>';
				html += '<th>&nbsp;'+_.List[i]['name']+'</th>';
				html += '<td align="center"><button onclick="requestObject.remove(\''+_.List[i]['id']+'\')">'+mfpLang['request']['del']+'</button></td>';
				html += '</tr>';
				if(mfpLang['request']['format']){
					var itemline = mfpLang['request']['format'];
					itemline = itemline.replace('$1',_.List[i]['id']);
					itemline = itemline.replace('$2',_.List[i]['name']);
					value += itemline + "\n";
				}
				else {
					value += '[ ' + _.List[i]['id'] + ' ] ' + _.List[i]['name'] + "\n";
				};
			};
			html = '<table class="mfp_shoppingcart"><thead><tr><td colspan="2">'+mfpLang['request']['h1']+'</td><td>'+mfpLang['request']['h2']+'</td></tr></thead><tbody>' + html + '</tbody></table>';
			mfp.$('mfp_request_cart').innerHTML = html;
			mfp.$('mfp_request_cart').style.display = 'block';
			mfp.$('mfp_request_cart_value').value = value;
		}
		else {
			mfp.$('mfp_request_cart').style.display = 'none';
		};
	},
	remove: function(id){
		mfp.call(mfp.$('mfpjs').src,'addon=request/request.js&callback=requestObject.get&remove='+id);
	},
	get: function(json){
		requestObject.List = json;
		requestObject.rebuild();
	},
	initialize: function(){
		if(!mfp.$('request_cart_value')){
			mfp.addhiddenObject('request_cart_value','',mfpLang['request']['cart']);
		};
		if(!document.getElementById('mfp_request_cart')){
			var elm = mfp.d.createElement('div');
			elm.id = 'mfp_request_cart';
			elm.innerHTML = 'Request';
			mfp.Mfp.insertBefore(elm,mfp.Mfp.firstChild);
		};
		mfp.call(mfp.$('mfpjs').src,'addon=request/request.js&callback=requestObject.get');
	}
};
mfp.extend.event('startup',
	function(){
		requestObject.initialize();
	}
);