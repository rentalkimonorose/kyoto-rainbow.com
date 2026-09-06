sub _QRCODE_GET {
	use LWP::UserAgent;
	my($text) = @_;
	my $uri = 'https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=' . &_QRCODE_ENCODE($text);
	my $qrcode = "";
	my $ua = LWP::UserAgent->new;
	$ua->timeout(30);
	$ua->agent($ENV{'HTTP_REFERER'});
	my $req = HTTP::Request->new(GET => $uri);
	$req->referer($ref);
	my $res = $ua->request($req);
	my $doc = $res->content;
	return $doc;
}
sub _QRCODE_ENCODE {
	my($text) = @_;
	$text =~ s/([^\w ])/'%' . unpack('H2', $1)/eg;
	$text =~ tr/ /+/;
	return $text;
}
sub _QRCODE_CHECK {
	my($binary) = @_;
	my $result = 1;
	unless ($binary =~ /^\x89\x50/ && $binary =~ /\x82$/){
		$result = 0;
	}
	return $result;
}
sub _QRCODE_SAVE {
	my($path,$data) = @_;
	flock(FH, LOCK_EX);
		open (OUT, ">${path}");
			binmode (OUT);
			print (OUT $data);
		close (OUT);
	flock(FH, LOCK_NB);
}
1;