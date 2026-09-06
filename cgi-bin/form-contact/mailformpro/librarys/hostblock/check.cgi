$_ENV{'mfp_hostname'} = &_GETHOST();
my @hostnames = split(/\n/,$config{'hostblock'});
@hostnames = grep $_ !~ /^\s*$/, @hostnames;
my $hostnameError = 0;
for(my $i=0;$i<@hostnames;$i++){
	if($_ENV{'mfp_hostname'} =~ /^.*?${hostnames[$i]}$/ig){
		$hostnameError = 1;
	}
}
if($hostnameError){
	$Error = 'HostnameCheck';
	if(-f $config{'hostblock_logfile'}){
		my @log = ($_ENV{'mfp_date'},$_ENV{'mfp_hostname'},$ENV{'REMOTE_ADDR'})
		&_ADDSAVE($config{'hostblock_logfile'},join("\t",@log));
	}
}
1;