// cart.js
var mfpFormObj = null;
function mfpCartAdd(obj){
	mfpFormObj = obj;
	var arr = [];
	var optionText = [];
	var optionCode = [];
	for(var i=0;i<obj.length;i++){
		var name = obj.elements[i].name;
		var value = obj.elements[i].value;
		var label = obj.elements[i].value;
		if(obj.elements[i].type == 'checkbox' || obj.elements[i].type == 'radio'){
			if(!obj.elements[i].checked){
				value = "";
			};
		}
		else if(obj.elements[i].type == 'select-one'){
			label = obj.elements[i].options[obj.elements[i].selectedIndex].text;
		};
		if(name.match(/name|item|qty|price|id/)){
			arr[name] = value;
		}
		else if(obj.elements[i].className.indexOf('option') > -1 && value != ''){
			optionText.push(name+":"+label);
			optionCode.push(value);
		};
		if(obj.elements[i].type == "submit"){
			obj.elements[i].disabled = true;
			obj.elements[i].className = "disabled";
			obj.elements[i].innerHTML = '<span>'+mfpCartAtt(obj.elements[i],'data-text')+'</span>';
		};
	};
	if(optionText.length > 0){
		arr['name'] += '(' + optionText.join(' / ') + ')';
		arr['item'] += '-' + optionCode.join('-');
	};
	var pram = [];
	for(var prop in arr){
		pram.push(prop + '=' + encodeURIComponent(arr[prop]));
	};
	//var pram = pram.join('&');
	mfpCartJson(obj.action+'&'+pram.join('&')+'&callback=mfpCartGet');
	return false;
};
function mfpCartJson(src){
	var script = document.createElement('script');
	script.async = false;
	script.type = 'text/javascript';
	script.src = src;
	script.charset = 'UTF-8';
	document.body.appendChild(script);
};
function mfpCartGet(json){
	var elm = document.createElement('a');
	elm.className = 'gocart';
	elm.innerHTML = '<span>'+mfpCartAtt(mfpFormObj,'data-text')+'</span>';
	elm.href = mfpCartAtt(mfpFormObj,'data-href');
	mfpFormObj.appendChild(elm);
};
function mfpCartAtt(obj,att){
	if(obj.getAttribute(att) != undefined)
		return obj.getAttribute(att);
	else
		return null;
};
