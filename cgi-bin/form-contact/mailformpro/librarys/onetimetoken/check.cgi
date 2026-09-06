my $tokenPath = $config{'onetimetoken.dir'} . &_SECPATH($_POST{'mfp_token'}) . '.cgi';
if(!(-f $tokenPath)){
	$_ErrorScreen = 1;
	$Error = 'OnetimeToken';
	$_COOKIE{'token'} = "";
}
else {
	$_COOKIE{'token'} = "";
	unlink $tokenPath;
}
1;