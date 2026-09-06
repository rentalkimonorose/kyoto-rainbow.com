$_GET{'q'} = &_SECURE($_GET{'q'});
if($_GET{'q'} ne $null && $_GET{'db'}){
	my $path = "$config{'dir.suggest'}$_GET{'db'}.txt";
	if(-f $path && !($_GET{'db'} =~ /[^a-zA-Z0-9]/si)){
		$_GET{'q'} =~ s/　/ /ig;
		my @db = &_DB($path);
		my @q = split(/ /,$_GET{'q'});
		for(my $i=0;$i<@q;$i++){
			@db = grep(/$q[$i]/ig,@db);
		}
		my @json = ();
		for(my $i=0;$i<@db;$i++){
			my @r = split(/\t/,$db[$i]);
			push @json,$r[0];
		}
		my $json = join("\,",@json);
		$js = <<"		__HTML__";
			mfpSuggestCallback(\{
				id: "$_GET{'id'}",
				result: '${json}'
			\});
		__HTML__
	
	}
	else {
		$js = "mfpSuggestCallbackError();";
	}
}
else {
	$js = 'mfpSuggestCallbackError();';
}
1;