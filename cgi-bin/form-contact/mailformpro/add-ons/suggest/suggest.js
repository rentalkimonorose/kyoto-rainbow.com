// サジェスト機能
// suggest.js 1.0.0 / 2018-12-08
var mfpSuggestToken = null;
var mfpSuggestBefoeToken = null;
var mfpSuggestJson = null;
var mfpSuggestPage = 10;
var mfpSuggestCurrentPage = 0;
mfp.extend.event('init',
	function(obj){
		if(obj.getAttribute('data-suggest')){
			var elm = mfp.d.createElement('div');
			elm.className = 'mfpSuggestWrapper';
			var elmChild = mfp.d.createElement('div');
			elmChild.className = 'mfpSuggestResult';
			elmChild.id = obj.id + '_result';
			elm.appendChild(elmChild);
			obj.parentNode.appendChild(elm);
			mfp.add(obj,"keyup",function(){
				clearTimeout(mfpSuggestToken);
				if(obj.value != "" && obj.value != mfpSuggestBefoeToken){
					mfpSuggestToken = setTimeout(function(){
						var CallBackElements = obj.id;
						var s = document.createElement("script");
						var u = '?';
						if(mfp.$('mfpjs').src.indexOf('?') > -1){
							u = '&';
						};
						if(!CallBackElements[3]){
							CallBackElements[3] = obj.name;
						};
						s.src = mfp.$('mfpjs').src + u + 'addon=suggest/suggest.js&q=' + encodeURIComponent(obj.value) + '&id=' + encodeURI(CallBackElements) + '&db=' + obj.getAttribute('data-suggest');
						mfpSuggestBefoeToken = obj.value;
						document.body.appendChild(s);
						mfp.$(obj.id+'_result').innerHTML = '<div class="prefLoading"></div>';
						mfp.$(obj.id+'_result').style.display = 'block';
					},500);
				}
			});
		}
	}
);
function mfpSuggestCallbackError(){
	alert("サジェスト機能の設定が有効ではありません");
}
function mfpSuggestCallback(json){
	mfpSuggestJson = json;
	var obj = document.getElementById(json["id"]+'_result');
	var result = json["result"].split(',');
	json["result"] = [];
	json["result"] = result;
	if(result != ''){
		obj.innerHTML = "";
		var i = 0;
		mfpSuggestCurrentPage = 0;
		for(i=0;i<json["result"].length && i < mfpSuggestPage;i++){
			var elm = mfp.d.createElement('div');
			elm.innerHTML = json["result"][i];
			var postcode = json["result"][i];
			var postcodejson = json;
			var resultObj = obj;
			elm.setAttribute("data-num",i);
			elm.onclick = function(){
				mfp.$(mfpSuggestJson["id"]).value = mfpSuggestJson["result"][this.getAttribute("data-num")];
				//callbackMFPZip(this.getAttribute("data-num"));
				resultObj.style.display = "none";
			}
			obj.appendChild(elm);
		}
		if(i < json["result"].length){
			var elm = mfp.d.createElement('div');
			elm.innerHTML = '次の候補を見る';
			elm.className = 'mfpSuggestNext';
			elm.onclick = mfpSuggestNextPage;
			obj.appendChild(elm);
		}
		obj.style.display = "block";
	}
	else {
		obj.innerHTML = "候補が見つかりませんでした";
		obj.style.display = "block";
	}
}
function mfpSuggestNextPage(){
	mfpSuggestCurrentPage++;
	var obj = document.getElementById(mfpSuggestJson["id"]+'_result');
	obj.innerHTML = "";
	var i = 0;
	for(i=0;(i+(mfpSuggestCurrentPage*mfpSuggestPage))<mfpSuggestJson["result"].length && i < mfpSuggestPage;i++){
		var n = i+(mfpSuggestCurrentPage*mfpSuggestPage);
		var elm = mfp.d.createElement('div');
		elm.innerHTML = mfpSuggestJson["result"][n];
		var resultObj = obj;
		elm.setAttribute("data-num",n);
		elm.onclick = function(){
			mfp.$(mfpSuggestJson["id"]).value = mfpSuggestJson["result"][this.getAttribute("data-num")];
			//callbackMFPZip(this.getAttribute("data-num"));
			resultObj.style.display = "none";
		}
		obj.appendChild(elm);
	}
	if((n+mfpSuggestPage) < mfpSuggestJson["result"].length){
		var elm = mfp.d.createElement('div');
		elm.innerHTML = '次の候補を見る';
		elm.className = 'mfpSuggestNext';
		elm.onclick = mfpSuggestNextPage;
		obj.appendChild(elm);
	}
}
