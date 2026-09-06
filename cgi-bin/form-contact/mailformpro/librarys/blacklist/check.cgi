my %blacklist = ();
$blacklist{'path'} = "$config{'blacklist.dir'}$ENV{'REMOTE_ADDR'}\.cgi";
if(-f $blacklist{'path'}){
	$_ErrorScreen = 1;
	$Error = 'BlackList';
}
1;