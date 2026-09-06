// サーチ機能
// search.js 1.0.0 / 2018-12-08
var mfpSearchToken = null;
var mfpSearchBefoeToken = null;
var mfpSearchJson = null;
var mfpSearchPage = 10;
var mfpSearchCurrentPage = 0;
var mfpSearchObjects = [];
var mfpSearchInterval = null;
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-search-for')){
			var id = obj.getAttribute('data-search-for');
			if(!mfpSearchObjects[id]){
				mfpSearchObjects[id] = [];
			};
			if(obj.type == 'text' || obj.type == 'search'){
				obj.onkeyup = function(){
					clearTimeout(mfpSearchInterval);
					mfpSearchInterval = setTimeout(mfpSearch.bind(this),1000);
				};
			};
			mfpSearchObjects[id].push(obj.id)
		};
	}
);
mfp.extend.event('change',
	function(obj){
		if(obj.getAttribute('data-search-for') && obj.value && obj.type != 'text' && obj.type != 'search'){
			mfpSearch(obj);
		};
	}
);
function mfpSearch(obj){
	obj = obj || this;
	clearTimeout(mfpSearchInterval);
	var id = obj.getAttribute('data-search-for');
	var db = mfp.$(id).getAttribute('data-search');
	var q = [];
	for(var i=0;i<mfpSearchObjects[id].length;i++){
		if(mfp.$(mfpSearchObjects[id][i]).type == 'select-one'){
			q.push(mfp.$(mfpSearchObjects[id][i]).value);
		}
		else if((mfp.$(mfpSearchObjects[id][i]).type == 'radio' || mfp.$(mfpSearchObjects[id][i]).type == 'checkbox') && mfp.$(mfpSearchObjects[id][i]).checked){
			q.push(mfp.$(mfpSearchObjects[id][i]).value);
		}
		else if(mfp.$(mfpSearchObjects[id][i]).value != '') {
			q.push(mfp.$(mfpSearchObjects[id][i]).value);
		};
	};
	var query = q.join(' ');
	var CallBackElements = obj.id;
	var s = document.createElement("script");
	var u = '?';
	if(mfp.$('mfpjs').src.indexOf('?') > -1){
		u = '&';
	};
	s.src = mfp.$('mfpjs').src + u + 'addon=search/search.js&q=' + encodeURIComponent(query) + '&id=' + encodeURI(id) + '&db=' + db;
	document.body.appendChild(s);
};
function mfpSearchCallbackError(){
	alert("サーチ機能の設定が有効ではありません");
};
function mfpSearchCallback(json){
	var results = json.result.split(',');
	mfp.$(json.id).length = results.length;
	for(var i=0;i<results.length;i++){
		mfp.$(json.id).options[i].text = results[i];
		mfp.$(json.id).options[i].value = results[i];
	};
};