my @referer = split(/\n/,$config{'referercheck'});
if($ENV{'HTTP_REFERER'} eq $null || grep(/^$ENV{'HTTP_REFERER'}$/,@referer) == 0){
	$Error = 'RefererCheck';
}
1;