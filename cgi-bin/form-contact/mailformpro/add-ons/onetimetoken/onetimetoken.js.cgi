$_GET{'callback'} =~ s/[^0-9A-Za-z\.\_]//ig;
if(-d $config{'onetimetoken.dir'} && $_GET{'callback'}){
	my $removeDir = $config{'onetimetoken.dir'};
	opendir DH, $removeDir;
	while (my $file = readdir DH) {
		next if $file =~ /^\.{1,2}$/;
		my $path = "${removeDir}${file}";
		if(!(-d $path)){
			my @file = split(/\./,$file);
			my $type = lc (pop @file);
			my $name = join('.',@file);
			my $time = (stat $path)[9];
			if($type eq 'cgi' && (time - $time) > $config{"onetimetoken.exp"}){
				unlink $path;
			}
		}
	}
	closedir DH;
	my $token = &_SECPATH($_COOKIE{'token'});
	my $tokenPath = $config{'onetimetoken.dir'} . $token . '.cgi';
	if(!(-f $tokenPath)){
		$token = time . $config{"onetimetoken.key"} . $ENV{'REMOTE_ADDR'} . $_COOKIE{'ses'};
		$token = &_HASH($token);
		$_COOKIE{'token'} = $token;
		$tokenPath = $config{'onetimetoken.dir'} . $token . '.cgi';
		&_SAVE($tokenPath,1);
	}
	$js = "$_GET{'callback'}(\'${token}\');";
}
1;