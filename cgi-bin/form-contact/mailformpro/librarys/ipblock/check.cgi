my %ipblock = ();
$ipblock{'path'} = "$config{'ipblock.dir'}$ENV{'REMOTE_ADDR'}\.cgi";
if(-f $ipblock{'path'}){
	$ipblock{'time'} = (stat($ipblock{'path'}))[9] + $config{'ipblock.time'};
	if(time < $ipblock{'time'}){
		$_ErrorScreen = 1;
		$Error = 'IPBlock';
	}
}
&_SAVE($ipblock{'path'},time);
1;