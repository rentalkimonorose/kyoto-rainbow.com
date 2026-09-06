foreach my $key(keys(%_POST)){
	for(my $cnt=0;$cnt<@TabooWords;$cnt++){
		if($_POST{$key} =~ /$TabooWords[$cnt]/si){
			$Error = $config{'taboowords.err'};
		}
	}
}
1;