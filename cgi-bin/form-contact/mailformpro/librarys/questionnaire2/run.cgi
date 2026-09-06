my @logs = &_DB($config{'questionnaire2.file'});
my %conflict = ();
foreach $key (keys(%questionnaire2)){
	my @keys = split(/\,/,$questionnaire2{$key});
	for(my $i=0;$i<@keys;$i++){
		if($_POST{$keys[$i]}){
			my $k = $_POST{$keys[$i]};
			my($lkey,$lname,$lqty) = split(/\t/,(grep(/^${key}\t${k}\t/,@logs))[0]);
			if(!$config{'questionnaire2.conflict'} || !$conflict{"${key}\t${k}"}){
				@logs = grep(!/^${key}\t${k}\t/,@logs);
				$lqty++;
				my @log = ($key,$k,$lqty);
				push @logs,join("\t",@log);
				$conflict{"${key}\t${k}"} = 1;
			}
		}
	}
}
@logs = sort { (split(/\t/,$a))[0] cmp (split(/\t/,$b))[0]} @logs;
&_SAVE($config{'questionnaire2.file'},join("\n",@logs));
1;