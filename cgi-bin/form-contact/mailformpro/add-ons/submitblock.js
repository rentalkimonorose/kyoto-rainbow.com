function checkProcess(){
	var requiredQty = 0;
	var ok = 0;
	for(var i=0;i<mfp.Names.length;i++){
		if(mfp.Elements[mfp.Names[i]].required){
			// required
			requiredQty++;
			if(mfp.Elements[mfp.Names[i]].check){
				ok++;
			};
		};
	};
	var submitObject = {
		disabled: true,
		className: 'mfp_submit_disable'
	};
	if(document.getElementById('mfp_status')){
		if(requiredQty - ok == 0){
			document.getElementById('mfp_status').innerHTML = '<div>送信の準備は完了です！内容をご確認の上、送信してください！</div>';
			submitObject.disabled = false;
			submitObject.className = 'mfp_submit_enabled';
		}
		else {
			document.getElementById('mfp_status').innerHTML = '<div>入力が必要な項目は、残り<strong>'+(requiredQty - ok)+'</strong>件です。</div>';
		};
	};
	var tObj = mfp.Mfp.getElementsByTagName('button');
	for(var i=0;i<tObj.length;i++){
		if(tObj[i].type == "submit" && tObj[i].getAttribute('data-submit-block')){
			if(submitObject.disabled){
				mfp.removeClassName(tObj[i],'mfp_submit_enable');
				mfp.addClassName(tObj[i],'mfp_submit_disable');
				tObj[i].innerHTML = tObj[i].getAttribute('data-submit-block');
				tObj[i].disabled = true;
			}
			else {
				mfp.removeClassName(tObj[i],'mfp_submit_disable');
				mfp.addClassName(tObj[i],'mfp_submit_enable');
				tObj[i].innerHTML = tObj[i].getAttribute('data-submit-block-enabled');
				tObj[i].disabled = false;
			};
		};
	};
}
mfp.extend.event('ready',
	function(){
		checkProcess();
	}
);
mfp.extend.event('change',
	function(){
		checkProcess();
	}
);
mfp.extend.event('blur',
	function(){
		checkProcess();
	}
);
