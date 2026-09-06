$_GET{'q'} = &_SECURE($_GET{'q'});
my $path = $config{'dir.estimate'} . $_GET{'item'} . '.txt.cgi';
if(-f $path && !($_GET{'item'} =~ /[^a-zA-Z0-9]/si)){
	my @db = &_DB($path);
	my $label = shift @db;
	my @label = split(/\t/,$label);
	if($_GET{'q'}){
		@db = grep(/\tEOF\t$_GET{'q'}/,@db);
	}
	if(!$_GET{'col'}){
		$_GET{'col'} = 5;
	}
	$label = $label[$_GET{'col'}];
	my %value = ();
	my @json = ();
	if(@db > 1){
		for(my $i=0;$i<@db;$i++){
			my @r = split(/\t/,$db[$i]);
			my $value = $r[$_GET{'col'}];
			if(!$value{$value}){
				push @json,"\"${value}\"";
				$value{$value} = 1;
			}
		}
		my $json = join("\,",@json);
		$_GET{'callback'} =~ s/[^0-9A-Za-z\.\_]//ig;
		$js = $_GET{'callback'} . "(\{items\: \[${json}\],id\: \"$_GET{'id'}\",column\: $_GET{'col'},label\: \"${label}\",query\: \"$_GET{'q'}\"\})";
	}
	else {
		my @r = split(/\t/,$db[0]);
		$js = "MfpEstimate\.finish(\{id\: \"$_GET{'id'}\",code\: \"${r[0]}\",name\: \"${r[1]}\",price\: ${r[2]},image\: \"${r[3]}\"\})";
	}
}
else {
	$js = 'MfpEstimate.error("' . $_GET{'item'} . '")';
}
1;