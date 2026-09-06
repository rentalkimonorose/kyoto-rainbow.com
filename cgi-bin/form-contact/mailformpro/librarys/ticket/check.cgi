if($_ENV{'mfp_cart'}){
	my $cart = $_ENV{'mfp_cart'};
	$cart =~ s/\,//ig;
	$cart =~ s/\t//ig;
	$cart =~ s/<->/\,/ig;
	$cart =~ s/\|\|/\n/ig;
	my @cart = split(/\n/,$cart);
	for(my $i=0;$i<@cart;$i++){
		my ($name,$id,$price,$qty) = split(/\,/,$cart[$i]);
		my @id = split(/_/,$id);
		if(!($id[0] =~ /[^a-zA-Z0-9\-]/) && !($id[1] =~ /[^a-zA-Z0-9\-]/) && @id == 2){
			if(-f "$config{'dir.ticket'}token/${id[0]}/${id[1]}.cgi"){
				$Error = 'TicketConflictError';
			}
		}
	}
}
1;