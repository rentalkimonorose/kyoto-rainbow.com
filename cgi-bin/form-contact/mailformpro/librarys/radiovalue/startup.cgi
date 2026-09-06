foreach $key (keys(%_POST)){
	my @value = split(/\n/,$_POST{$key});
	for(my $i=0;$i<@value;$i++){
		$_ENV{"${key}_${value[$i]}"} = 1;
	}
}
1;