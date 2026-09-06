&_GET;
my $paymentKey = "";
my $resultCode = "";
if(-f "$config{'veritrans.Token.dir'}$_GET{'token'}.cgi"){
	my $currentTime = time;
	if($currentTime < ((stat("$config{'veritrans.Token.dir'}$_GET{'token'}.cgi"))[9]+$config{'veritrans.expire'})){
		$config{'buffer'} = &_LOAD("$config{'veritrans.Token.dir'}$_GET{'token'}.cgi");
		if($config{'buffer'} =~ /^(.*?)\n\[\[(.*?)\]\]/si){
			$_ENV{'mfp_serial'} = $1;
			$config{'buffer'} = $2;
			&_POST;
			
			if($_GET{'cancel'}){
				print "Location: $config{'veritrans.CancelPage'}\n\n";
				unlink "$config{'veritrans.Token.dir'}$_GET{'token'}.cgi";
				my $subject = "\[ $_ENV{'mfp_serial'} \] 決済がキャンセルされました";
				my $body = "受付番号 $_ENV{'mfp_serial'} の決済がキャンセルされました";
				for(my $i=0;$i<@mailto;$i++){
					&_SENDMAIL($mailto[$i],$config{'veritrans.NoticeFrom'},$config{'veritrans.NoticeFrom'},$subject,$body);
				}
			}
			elsif($_GET{'method'} eq 'callback' && $_GET{'tran_code'} ne $null && $_GET{'amount'} ne $null){
				$config{'ThanksPage'} = sprintf($config{'ThanksPage'},$_ENV{'mfp_serial'});
				print "Location: $config{'ThanksPage'}\n\n";
				unlink "$config{'veritrans.Token.dir'}$_GET{'token'}.cgi";
				my $subject = "\[ $_ENV{'mfp_serial'} \] 決済が完了しました";
				my $body = "受付番号 $_ENV{'mfp_serial'} の決済が完了しました";
				for(my $i=0;$i<@mailto;$i++){
					&_SENDMAIL($mailto[$i],$config{'veritrans.NoticeFrom'},$config{'veritrans.NoticeFrom'},$subject,$body);
				}
			}
			else {
				my $uri = &_MFP2URI("module=veritrans&token=$_GET{'token'}");
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
				use MIME::Base64;
				use LWP::UserAgent;
				use HTTP::Request::Common qw(POST);
				use HTTP::Request;
				my $AUTH_STRING = encode_base64($config{'veritrans.ServerKey'} . ":");
				my $ua = LWP::UserAgent->new;
				$ua->default_header('Authorization' => "Basic ${AUTH_STRING}");
				$ua->default_header('Content-Type' => "application/json; charset=utf-8");
				my $url = "https://pay.veritrans.co.jp/pop/v1/payment-key";
my $json = <<__POST_JSON__;
{
    "order_id": "$_ENV{'mfp_serial'}",
    "gross_amount": ${itemPrice},
    "success_url": "${uri}&method=callback",
    "failure_url": "${uri}&method=callback&cancel=1",
    "incomplete_url": "${uri}&method=callback&cancel=1"
}
__POST_JSON__
				$json =~ s/\t//ig;
				my $req= HTTP::Request->new(POST => $url);
				$req->content($json);
				my $result = $ua->request($req)->as_string;
				if($result =~ /\"payment_key\"\:\"(.*?)\"/){
					$paymentKey = $1;
				}
				elsif($result =~ /\"result_code\"\:\"(.*?)\"/){
					$resultCode = $1;
				}
				push @html,"<form>";
				push @html,"<img src=\"data:image/png;base64,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\">";
				my $uri = &_MFP2URI("module=veritrans&token=$_GET{'token'}");
				push @html,"</form>";
				my $parts = join("\n",@html);
				my $html = &_LOAD("./librarys/veritrans/template.tpl");
				$html =~ s/_%%clientkey%%_/$config{'veritrans.ClientKey'}/ig;
				$html =~ s/_%%paymentkey%%_/$paymentKey/ig;
				$html =~ s/_%%resultcode%%_/$resultCode/ig;
				$html =~ s/_%%success%%_//ig;
				$html =~ s/_%%failure%%_//ig;
				$html =~ s/_%%incomplete%%_//ig;
				$html =~ s/_%%main%%_/$parts/ig;
				print "Pragma: no-cache\n";
				print "Cache-Control: no-cache\n";
				print "Content-type: text/html; charset=UTF-8\n\n";
				print $html;
			}
		}
		else {
			unlink "$config{'veritrans.Token.dir'}$_GET{'token'}.cgi";
			&_Error(1);
		}
	}
	else {
		unlink "$config{'veritrans.Token.dir'}$_GET{'token'}.cgi";
		&_Error(2);
	}
}
else {
	&_Error(3);
}
1;