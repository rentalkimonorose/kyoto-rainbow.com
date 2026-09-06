if($_POST{$config{'veritrans.PaymentType'}} eq $config{'veritrans.PaymentName'}){
	my $token = &_HASH(time . "." . $ENV{'REMOTE_ADDR'} . "." . $_ENV{'mfp_serial'});
	$config{'ThanksPageBackyard'} = $config{'ThanksPage'};
	$config{'ThanksPage'} = &_MFP2URI("module=veritrans&token=${token}");
	&_SAVE("$config{'veritrans.Token.dir'}${token}.cgi","$_ENV{'mfp_serial'}\n\[\[${buffer}\]\]");
}
## Remove until expired Files
my $removeDir = $config{'veritrans.Token.dir'};
opendir DH, $removeDir;
while (my $file = readdir DH) {
	next if $file =~ /^\.{1,2}$/;
	my $path = "${removeDir}${file}";
	if(!(-d $path)){
		my @file = split(/\./,$file);
		my $type = lc (pop @file);
		my $name = join('.',@file);
		my $time = (stat $path)[9];
		if($type eq 'cgi' && (time - $time) > $config{'veritrans.expire'}){
			unlink $path;
		}
	}
}
closedir DH;

1;