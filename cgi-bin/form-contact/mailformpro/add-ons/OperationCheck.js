var mfpElementsList = new Array();
var mfpElementsListCheck = new Object();
function mfpElementsListPrompt(){
	prompt('MailformPro Elements List',mfpElementsList.join(','));
};
function mfpOperationCheckDetail(obj){
	obj.style.display = 'none';
	mfp.$('mfp_OperationCheck_inner').style.display = 'block';
};
function mfpOperationCheckSheet(){
	var tObj = mfp.$('mfpOperationCheckSheet').getElementsByTagName('input');
	var status = true;
	for(var i=0;i<tObj.length;i++){
		if(!tObj[i].checked){
			status = false;
		};
	};
	if(status){
		setTimeout(function(){
			alert("確認はバッチリですね！ではconfig.cgiの\npush @AddOns,'OperationCheck.js';\nを削除またはコメントアウトし、この表示を消しましょう。\nたくさんのお問い合わせが来ることを祈っています札幌から！");
		},100);
	};
};
var mfpOperationCheckObject = [];
mfp.extend.event('ready',
	function(){
		var version = '4.2.7';
		var elm = mfp.d.createElement('div');
		elm.id = 'mfp_OperationCheck';
		mfp.Mfp.parentNode.insertBefore(elm,mfp.$('mfp_warning'));
		var par = Math.round(mfp.Analytics.requiredQty/mfp.Analytics.qty*10000)/100;
		var src = mfp.$('mfpjs').src + '?module=check';
		if(mfp.$('mfpjs').src.indexOf('?') > -1){
			src = mfp.$('mfpjs').src + '&module=check';
		};
		var innerHTML = '<strong>メールフォームプロ 動作チェック アドオン</strong>';
		innerHTML += '<p>mailformpro.cgi version.'+version+' は正常に動作しています。 <button type="button" onclick="mfpOperationCheckDetail(this)">[ 詳細を表示する ]</button></p>';
		innerHTML += '<div id="mfp_OperationCheck_inner">';
		innerHTML += '<p><a href="'+src+'" target="_blank">[ CGI動作チェックモジュールを実行する ]</a> <button onclick="mfpElementsListPrompt()" type="button">[ エレメントリストを取得 ]</button></p>';
		innerHTML += '<p>この表示はconfig.cgiの設定により消すことができます。っていうか消して。</p>';
		innerHTML += '<p>このフォームには'+mfp.Analytics.qty+'個のエレメントが配置されており'+mfp.Analytics.requiredQty+'個('+par+'%)が必須項目です。</p>';
		var ElementsType = new Array();
		for(var prop in mfp.Analytics.type){
			ElementsType.push(prop+"/"+mfp.Analytics.type[prop]);
		};
		innerHTML += '<p>'+ElementsType.join('、')+'で構成されています。</p>';
		innerHTML += '</div>';
		innerHTML += '<ul id="mfpOperationCheckSheet">';
		innerHTML += '<li><label><input type="checkbox" onchange="mfpOperationCheckSheet()"> sendmailのパスの設定はお済みですか？</label></li>';
		innerHTML += '<li><label><input type="checkbox" onchange="mfpOperationCheckSheet()"> フォームの送信先メールアドレスは変更しましたか？</label></li>';
		innerHTML += '<li><label><input type="checkbox" onchange="mfpOperationCheckSheet()"> 自動返信メールの署名は変更しましたか？</label></li>';
		innerHTML += '<li><label><input type="checkbox" onchange="mfpOperationCheckSheet()"> メールの送信テストは行いましたか？</label></li>';
		innerHTML += '</ul>';
		elm.innerHTML = innerHTML;
		
		mfp.css(mfp.$('mfp_OperationCheck'),{
			"borderRadius": "3px",
			"fontSize": "16px",
			"lineHeight": "1.5em",
			"color": "#090",
			"margin": "10px auto",
			"boxShadow": "0px 2px 10px #666",
			"textAlign": "left",
			"padding": "10px",
			"backgroundColor": '#222'
		});
	}
);
mfp.extend.event('init',
	function(e){
		if(e.name && !mfpElementsListCheck[e.name]){
			mfpElementsList.push(e.name);
			mfpElementsListCheck[e.name] = true;
		}
	}
);
