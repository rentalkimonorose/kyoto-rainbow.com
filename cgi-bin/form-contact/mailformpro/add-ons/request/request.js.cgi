$_GET{'callback'} =~ s/[^0-9A-Za-z\.\_]//ig;
$_GET{'id'} = &_SECURE($_GET{'id'});
if(-d $config{'dir.request'} && $_GET{'callback'}){
	my $reqpath = "$config{'dir.request'}$_COOKIE{'SES'}.cgi";
	my @req = ();
	if(-f $reqpath){
		@req = &_DB($reqpath);
	}
	if($_GET{'id'} && $_GET{'name'} && &_SECSTR($_GET{'id'})){
		$_GET{'id'} = &_SANITIZING($_GET{'id'});
		$_GET{'name'} = &_SANITIZING($_GET{'name'});
		@req = grep(!/^$_GET{'id'}\t/,@req);
		my $image = 0;
		if($_GET{'image'}){
			$image = 1;
		}
		my @item = ($_GET{'id'},$_GET{'name'},$image);
		push @req,join("\t",@item);
	}
	if($_GET{'remove'}){
		$_GET{'remove'} = &_SANITIZING($_GET{'remove'});
		@req = grep(!/^$_GET{'remove'}\t/,@req);
	}
	
	## Callback Request
	my @json = ();
	@req = sort { (split(/\t/,$a))[0] cmp (split(/\t/,$b))[0]} @req;
	for(my $i=0;$i<@req;$i++){
		my($id,$name,$image) = split(/\t/,$req[$i]);
		push @json,"\{'id': '${id}','name': '${name}','image': ${image}\}";
	}
	
	$js = "$_GET{'callback'}(\[" . join(",",@json) . "\]);console.log(\[" . join(",",@json) . "\]);";
	if(@json > 0){
		&_SAVE("$config{'dir.request'}$_COOKIE{'SES'}.cgi",join("\n",@req));
	}
	else {
		unlink "$config{'dir.request'}$_COOKIE{'SES'}.cgi";
	}
}
1;