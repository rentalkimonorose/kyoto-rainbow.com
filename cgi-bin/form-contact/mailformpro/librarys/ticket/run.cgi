if($_ENV{'mfp_cart'}){
	my @cart = split(/\n/,$_ENV{'mfp_cart'});
	for(my $i=0;$i<@cart;$i++){
		my ($name,$id,$price,$qty) = split(/\,/,$cart[$i]);
		my @id = split(/_/,$id);
		if(!($id[0] =~ /[^a-zA-Z0-9\-]/) && !($id[1] =~ /[^a-zA-Z0-9\-]/) && @id == 2){
			mkdir "$config{'dir.ticket'}token/${id[0]}/";
			&_SAVE("$config{'dir.ticket'}token/${id[0]}/${id[1]}.cgi",$_ENV{'mfp_serial'});
		}
	}
}
1;