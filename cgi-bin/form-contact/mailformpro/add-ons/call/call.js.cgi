$_GET{'q'} = &_SECURE($_GET{'q'});
if($_GET{'q'} ne $null && $_GET{'db'}){
	my $path = "$config{'dir.call'}$_GET{'db'}.txt";
	if(-f $path && !($_GET{'db'} =~ /[^a-zA-Z0-9]/si)){
		$_GET{'q'} =~ s/　/ /ig;
		my @db = &_DB($path);
		@db = grep(/^$_GET{'q'}/ig,@db);
		if(@db == 1){
			my @r = split(/\t/,$db[0]);
			$js = <<"			__HTML__";
				mfpCallCallback(\{
					target: '$_GET{'id'}',
					id: '${r[0]}',
					name: '${r[1]}',
					price: ${r[2]}
				\});
			__HTML__
		}
		else {
			$js = "mfpCallCallbackUnmatch('$_GET{'id'}');";
		}
	}
	else {
		$js = "mfpCallCallbackError();";
	}
}
else {
	$js = 'mfpCallCallbackError();';
}
1;