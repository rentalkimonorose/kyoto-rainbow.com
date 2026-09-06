my $path = $config{'dir.ticket'} . $_GET{'file'} . '.txt.cgi';
if(-f $path && !($_GET{'file'} =~ /[^a-zA-Z0-9]/si)){
	my @db = ();
	## cache
	if($config{'ticket.encode'}){
		my $cache = $path . '.cache.cgi';
		my $ct = (stat $cache)[9];
		my $ot = (stat $path)[9];
		if($ot > $ct){
			## create cache
			my $data = &_LOAD($path);
			use Encode;
			Encode::from_to($data,'cp932','utf8');
			&_SAVE($cache,$data);
		}
		$path = $cache;
	}
	@db = &_DB($path);
	if($_GET{'item'}){
		## map
		my @id = split(/\t/,$db[0]);
		my $index = 0;
		my @json = ();
		for(my $i=4;$i<@id;$i++){
			if($id[$i] eq $_GET{'item'}){
				$index = $i;
				break;
			}
		}
		for(my $i=6;$i<@db;$i++){
			my @r = split(/\t/,$db[$i]);
			my $id = $r[0];
			my $name = $r[1];
			my $x = $r[2];
			my $y = $r[3];
			my $price = $r[$index];
			if(!($price =~ /[^a-zA-Z0-9]/si)){
				$price = $r[$index];
			}
			else {
				$price = "false";
			}
			if(-f "$config{'dir.ticket'}token/$_GET{'item'}/${id}.cgi"){
				$price = "false";
			}
			my @j = ("id: \"${id}\"","name: \"${name}\"","x: ${x}","y: ${y}","price: ${price}");
			my $j = "{" . join("\,",@j) . "}";
			push @json,$j;
		}
		my $json = join("\,",@json);
		$_GET{'callback'} =~ s/[^0-9A-Za-z\.\_]//ig;
		$js = $_GET{'callback'} . "(\{ticket\: \[${json}\],id\: \"$_GET{'id'}\"\})";
	}
	else {
		## select
		my @label = split(/\t/,$db[0]);
		my @limit = split(/\t/,$db[1]);
		my @text1 = split(/\t/,$db[2]);
		my @text2 = split(/\t/,$db[3]);
		my @text3 = split(/\t/,$db[4]);
		my @text4 = split(/\t/,$db[5]);
		my @json = ();
		my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
		my $date = sprintf("%04d-%02d-%02d %02d:%02d",$year+1900,$mon+1,$day,$hour,$min);
		for(my $i=4;$i<@label;$i++){
			if($date le $limit[$i]){
				my @j = ("id: \"${label[$i]}\"","text1: \"${text1[$i]}\"","text2: \"${text2[$i]}\"","text3: \"${text3[$i]}\"","text4: \"${text4[$i]}\"");
				my $j = "{" . join("\,",@j) . "}";
				push @json,$j;
			}
		}
		my $json = join("\,",@json);
		$js = $_GET{'callback'} . "(\{items\: \[${json}\],id\: \"$_GET{'id'}\"\})";
	}
}
else {
	$js = 'MfpTicket.error("' . $_GET{'file'} . '")';
}
1;