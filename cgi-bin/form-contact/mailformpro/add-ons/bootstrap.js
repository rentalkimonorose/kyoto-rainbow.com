mfpConfigs["SizeAjustPx"] = null;
mfpConfigs['mfpButton'] = '<div class="mfp_buttons"><button id="mfp_button_send" class="mfp_element_button btn btn-primary" onclick="mfp.sendmail()">'+mfpLang['ButtonSend']+'</button>&nbsp;<button id="mfp_button_cancel" class="mfp_element_button btn btn-secondary" onclick="mfp.cancel()">'+mfpLang['ButtonCancel']+'</button></div>';
mfpLang['ConfirmTitle'] = '<div class="modal-header"><h5 class="modal-title">入力内容をご確認ください</h5><button type="button" class="close" onclick="mfp.cancel()"><span aria-hidden="true">×</span></button></div>';
mfp.extend.event('ready',
	function(){
		var elms = mfp.byClassName(mfp.Mfp,'mfp_err');
		for(var i=0;i<elms.length;i++){
			elms[i].parentNode.style.position = 'relative';
			elms[i].style.position = 'absolute';
			elms[i].style.right = '0px';
			elms[i].style.bottom = '-2em';
			elms[i].style.lineHeight = '1em';
		};
		//mfp.$('mfp_overlay_inner').className = 'modal-dialog';
		mfp.$('mfp_overlay_inner').role = 'document';
	}
);
