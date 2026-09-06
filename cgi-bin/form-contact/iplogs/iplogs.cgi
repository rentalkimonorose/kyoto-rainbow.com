#!/usr/bin/perl
## 
%_ENV = ();
&_ENV;

## set Uri
my %uri = ();
$uri{'test'} = 'https://www.synck.com/index.html';

## File Size Limit Bytes
## 1MB = 1048576 Byte
$_ENV{'size'} = 1048576;

if($_ENV{'query'}){
	if($uri{$_ENV{'query'}}){
		my @log = ($_ENV{'date'},$_ENV{'ip'},"$_ENV{'query'} Click");
		&_LOG(join("\t",@log));
		print "Location: $uri{$_ENV{'query'}}\n\n";
	}
	elsif(index($_ENV{'referer'},$_ENV{'domain'}) > -1){
		my @log = ($_ENV{'date'},$_ENV{'ip'},$_ENV{'query'});
		&_LOG(join("\t",@log));
		open(IMG,"iplogs.img.gif");
		my $byte = -s "iplogs.img.gif";
		print "Content-type: image/gif\n";
		print "Content-length: $byte\n\n";
		print <IMG>;
		close(IMG);
	}
	else {
		print "Content-type: text/html; charset=UTF-8\n\n";
	}
}
else {
	print "Pragma: no-cache\n";
	print "Cache-Control: no-cache\n";
	print "Content-type: text/javascript; charset=UTF-8\n\n";
	print "if(document.referrer) document.write('<img src=\"$_ENV{'uri'}?'+document.referrer+'\" style=\"position: absolute;\">');";
}
exit;
sub _ENV {
	$_ENV{'file'} = './iplogs.dat.cgi';
	$_ENV{'domain'} = $ENV{'SERVER_NAME'};
	$_ENV{'uri'} = '//' . $ENV{'SERVER_NAME'} . $ENV{'SCRIPT_NAME'};
	$_ENV{'referer'} = $ENV{'HTTP_REFERER'};
	$_ENV{'ip'} = $ENV{'REMOTE_ADDR'};
	my($protocol,$referer) = split(/\/\//,$ENV{'QUERY_STRING'});
	$referer =~ s/^$_ENV{'domain'}\//\//ig;
	$referer =~ s/\n//ig;
	$referer =~ s/\t//ig;
	if($referer){
		$_ENV{'query'} = $referer;
	}
	else {
		$_ENV{'query'} = $ENV{'QUERY_STRING'};
	}
	
	my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
	$_ENV{'date'} = sprintf("%04d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$day,$hour,$min,$sec);
	$_ENV{'day'} = sprintf("%04d-%02d-%02d",$year+1900,$mon+1,$day);
	
	($sec,$min,$hour,$day,$mon,$year) = localtime(time - (60*60*24));
	$_ENV{'yesterday'} = sprintf("%04d-%02d-%02d",$year+1900,$mon+1,$day);
}
sub _LOG {
	my($log) = @_;
	if((-s $_ENV{'file'}) > $_ENV{'size'} && ($_ENV{'size'})){
		my @logs = &_LOAD($_ENV{'file'});
		my @l1 = grep(/^$_ENV{'day'}/,@logs);
		my @l2 = grep(/^$_ENV{'yesterday'}/,@logs);
		@logs = (@l1,@l2);
		push @logs,$log;
		&_SAVE($_ENV{'file'},join("\n",@logs));
	}
	else {
		&_ADDSAVE($_ENV{'file'},$log);
	}
}
sub _ADDSAVE {
	my($path,$str) = @_;
	chmod 0777,$path;
	flock(FH, LOCK_EX);
		open(FH,">>${path}");
			print FH $str . "\n";
		close(FH);
	flock(FH, LOCK_NB);
	chmod 0600,$path;
}
sub _LOAD {
	my($path) = @_;
	my @str = ();
	flock(FH, LOCK_EX);
		open(FH,$path);
			@str = <FH>;
		close(FH);
	flock(FH, LOCK_NB);
	my $str = join('',@str);
	$str =~ s/\r//ig;
	return split(/\n/,$str);
}
sub _SAVE {
	my($path,$str) = @_;
	chmod 0777,$path;
	open(FH,"+< ${path}");
		flock(FH,2);
		seek(FH,0,0);
		print FH $str . "\n";;
		truncate(FH,tell(FH));
	close(FH);
	chmod 0600,$path;
}
1;