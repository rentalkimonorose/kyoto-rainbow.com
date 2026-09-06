&_GET;
if(-f "$config{'yamato.Token.dir'}$_GET{'token'}.cgi"){
	my $currentTime = time;
	if($currentTime < ((stat("$config{'yamato.Token.dir'}$_GET{'token'}.cgi"))[9]+$config{'yamato.expire'})){
		$config{'buffer'} = &_LOAD("$config{'yamato.Token.dir'}$_GET{'token'}.cgi");
		if($config{'buffer'} =~ /^(.*?)\n\[\[(.*?)\]\]/si){
			$_ENV{'mfp_serial'} = $1;
			$config{'buffer'} = $2;
			my $order_no = $_POST{'order_no'};
			my $settle_price = $_POST{'settle_price'};
			my $settle_result = $_POST{'settle_result'};
			&_POST;
			&_MAILTEXT;
			if($_GET{'cancel'}){
				print "Location: $config{'yamato.CancelPage'}\n\n";
				unlink "$config{'yamato.Token.dir'}$_GET{'token'}.cgi";
				my $subject = "\[ $_ENV{'mfp_serial'} \] 決済がキャンセルされました";
				my $body = "受付番号 $_ENV{'mfp_serial'} の決済がキャンセルされました";
				for(my $i=0;$i<@mailto;$i++){
					&_SENDMAIL($mailto[$i],$config{'yamato.NoticeFrom'},$config{'yamato.NoticeFrom'},$subject,$body);
				}
			}
			elsif($_GET{'method'} eq 'callback'){
				$config{'ThanksPage'} = sprintf($config{'ThanksPage'},$_ENV{'mfp_serial'});
				print "Location: $config{'ThanksPage'}\n\n";
				unlink "$config{'yamato.Token.dir'}$_GET{'token'}.cgi";
				my $subject = "\[ $_ENV{'mfp_serial'} \] 決済が完了しました";
				my $body = "受付番号 $_ENV{'mfp_serial'} の決済が完了しました\nクロネコWebコレクト 管理画面より決済結果をご確認ください。";
				for(my $i=0;$i<@mailto;$i++){
					&_SENDMAIL($mailto[$i],$config{'yamato.NoticeFrom'},$config{'yamato.NoticeFrom'},$subject,$body);
				}
			}
			else {
				my @items = split(/\|\|/,$_ENV{'mfp_cart'});
				my $itemName = "";
				my $itemQty = 0;
				my $itemPrice = 0;
				my $itemOther = 0;
				for(my $i=0;$i<@items;$i++){
					my($name,$id,$price,$qty) = split(/<->/,$items[$i]);
					$itemQty += $qty;
					$itemPrice += ($price * $qty);
					if(!$itemName){
						$itemName = $name;
					}
					else {
						$itemOther = 1;
					}
				}
				my @html = ("<form method=\"post\" id=\"yamato\" action=\"$config{'yamato.Uri'}\" accept-charset=\"Shift_JIS\">");
				push @html,"<img src=\"data:image/gif;base64,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\">";
				if($itemOther){
					push @html,"<input type=\"hidden\" name=\"goods_name\" value=\"${itemName}など${itemQty}点の商品\">";
				}
				else {
					push @html,"<input type=\"hidden\" name=\"goods_name\" value=\"${itemName}\">";
				}
				my $uri = &_MFP2URI("module=yamato&token=$_GET{'token'}");
				push @html,"<input type=\"hidden\" name=\"settle_price\" value=\"${itemPrice}\">";
				push @html,"<input type=\"hidden\" name=\"order_no\" value=\"$_ENV{'mfp_serial'}\">";
				push @html,"<input type=\"hidden\" name=\"success_url\" value=\"${uri}&method=callback\">";
				push @html,"<input type=\"hidden\" name=\"failure_url\" value=\"${uri}&method=callback&cancel=1\">";
				push @html,"<input type=\"hidden\" name=\"cancel_url\" value=\"${uri}&method=callback&cancel=1\">";
				push @html,"<input type=\"hidden\" name=\"TRS_MAP\" value=\"$_YAMATO_PAYMENT{'TRS_MAP'}\">";
				push @html,"<input type=\"hidden\" name=\"trader_code\" value=\"$_YAMATO_PAYMENT{'trader_code'}\">";
				
				if($_TEXT{'yamato_buyer_name_kanji'}){
					push @html,"<input type=\"hidden\" name=\"buyer_name_kanji\" value=\"$_TEXT{'yamato_buyer_name_kanji'}\">";
				}
				if($_TEXT{'yamato_buyer_name_kana'}){
					push @html,"<input type=\"hidden\" name=\"buyer_name_kana\" value=\"$_TEXT{'yamato_buyer_name_kana'}\">";
				}
				if($_TEXT{'yamato_buyer_email'}){
					push @html,"<input type=\"hidden\" name=\"buyer_email\" value=\"$_TEXT{'yamato_buyer_email'}\">";
				}
				if($_TEXT{'yamato_buyer_tel'}){
					my $tel = $_TEXT{'yamato_buyer_tel'};
					$tel =~ s/ー//ig;
					$tel =~ s/－//ig;
					$tel =~ s/-//ig;
					$tel =~ s/\(//ig;
					$tel =~ s/\)//ig;
					push @html,"<input type=\"hidden\" name=\"buyer_tel\" value=\"${tel}\">";
				}
				push @html,"<button>決済画面に進む</button>";
				push @html,"</form>";
				my $parts = join("\n",@html);
				my $html = &_LOAD("./librarys/yamato/template.tpl");
				$html =~ s/_%%main%%_/$parts/ig;
				print "Pragma: no-cache\n";
				print "Cache-Control: no-cache\n";
				print "Content-type: text/html; charset=UTF-8\n\n";
				print $html;
			}
		}
		else {
			unlink "$config{'yamato.Token.dir'}$_GET{'token'}.cgi";
			&_Error(1);
		}
	}
	else {
		unlink "$config{'yamato.Token.dir'}$_GET{'token'}.cgi";
		&_Error(2);
	}
}
else {
	&_Error(3);
}
1;