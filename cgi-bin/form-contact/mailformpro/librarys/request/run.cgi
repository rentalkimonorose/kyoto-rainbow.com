if(-d $config{'dir.request'}){
	my $path = "$config{'dir.request'}$_COOKIE{'SES'}.cgi";
	if(-f $path){
		unlink $path;
	}
}
1;