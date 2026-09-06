sub _MAILHEADER {
	my($to,$from,$name,$subject,$body,$attached,$htmlmail) = @_;
	my $str;
	$subject = &_MIME($subject,'UTF-8');
	$from = &_MIME("${name}",'UTF-8') . "<${from}>";
	if($config{'breakcode'}){
		$body =~ s/\n/$config{'breakcode'}/ig;
	}
	$body = encode_base64($body);
	
	$str .= "Subject: ${subject}\n";
	$str .= "From: ${from}\n";
	$str .= "To: ${to}\n";
	if($config{'bcc'} ne $null && $config{'bcc'} ne $mailto){
		$str .= "Bcc: $config{'bcc'}\n";
	}
	if($config{'Notification'}){
		$str .= "Disposition-Notification-To: $config{'Notification'}\n";
	}
	$str .= "MIME-Version: 1.0\n\n";
	$str .= "Content-Type: text/plain; charset=\"UTF-8\"\n";
	$str .= "Content-Transfer-Encoding: Base64\n";
	$str .= "Content-Disposition: inline\n\n";
	$str .= "${body}\n";
	return $str;
}
1;