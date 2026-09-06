my @json = ();
foreach $key ( keys( %_POST ) ) {
	my $val = &_SANITIZING($_POST{$key});
	$val =~ s/&#x2c;/\,/g;
	if(index($key,'mfp_') == -1 && $key ne 'resbody'){
		push @json,"\'${key}\': \'${val}\'\n";
	}
}
if($config{'thanks.env'}){
	foreach $key ( keys( %_ENV ) ) {
		my $val = &_SANITIZING($_ENV{$key});
		$val =~ s/&#x2c;/\,/g;
		my $name = $key;
		if($config{'thanks.env.jp'}){
			$name = &_NAME($key);
		}
		push @json,"\'${name}\': \'${val}\'\n";
	}
}
my $json = '{' . join(',',@json) . '}';
&_SAVE($config{'data.dir'} . "json/$_COOKIE{'SES'}.cgi",$json);

## Remove until expired Files
my $removeDir = $config{'data.dir'} . 'json/';
opendir DH, $removeDir;
while (my $file = readdir DH) {
	next if $file =~ /^\.{1,2}$/;
	my $path = "${removeDir}${file}";
	if(!(-d $path)){
		my @file = split(/\./,$file);
		my $type = lc (pop @file);
		my $name = join('.',@file);
		my $time = (stat $path)[9];
		if($type eq 'cgi' && (time - $time) > $config{'thanks.expire'}){
			unlink $path;
		}
	}
}
closedir DH;
1;