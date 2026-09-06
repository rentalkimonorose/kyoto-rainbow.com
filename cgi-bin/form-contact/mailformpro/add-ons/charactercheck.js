function mfp_char1byte(str){
	for(var i=0;i<str.length;i++){
		if(escape(str.charAt(i)).length >= 4){
			return true;
			break;
		};
	};
	return false;
};
function mfp_char2byte(str){
	for(var i=0;i<str.length;i++){
		if(!(escape(str.charAt(i)).length >= 4)){
			return true;
			break;
		};
	};
	return false;
};

mfp.extend.event('check',
	function(obj){
		if(obj.name != ""){
			if((mfp.Elements[obj.name].type == "text" || mfp.Elements[obj.name].type == "textarea" || mfp.Elements[obj.name].type == "email") && obj.getAttribute('data-charcheck') && obj.value != "" && obj.value != obj.defaultValue){
				// data-charcheck="digit" 数字のみ
				// data-charcheck="alphabet" 英語のみ
				// data-charcheck="digit_and_alphabet" 英語と数字のみ(記号含まず)
				// data-charcheck="kana" 全角カタカナとスペースのみ---edit poo

				if(obj.value.match(/[^0-9]/) && obj.getAttribute('data-charcheck') == 'digit')
					mfp.ExtendErrorMsg = '$name に数字以外の文字が入力されています。';
				else if(obj.value.match(/[^A-Za-z ]/) && obj.getAttribute('data-charcheck') == 'alphabet')
					mfp.ExtendErrorMsg = '$name に英字以外の文字が入力されています。';
				else if(obj.value.match(/[^A-Za-z0-9]/) && obj.getAttribute('data-charcheck') == 'digit_and_alphabet')
					mfp.ExtendErrorMsg = '$name に英数字以外の文字が入力されています。';
				else if(obj.value.match(/[^ァ-ヶー 　]/) && obj.getAttribute('data-charcheck') == 'kana')
					mfp.ExtendErrorMsg = '$name にカタカナ以外の文字が入力されています。';
				else if(mfp_char1byte(obj.value) && obj.getAttribute('data-charcheck') == 'hankaku')
					mfp.ExtendErrorMsg = '$name に半角以外の文字が入力されています。';
				else if(mfp_char2byte(obj.value) && obj.getAttribute('data-charcheck') == 'zenkaku')
					mfp.ExtendErrorMsg = '$name に全角以外の文字が入力されています。';
			}
		}
	}
);
