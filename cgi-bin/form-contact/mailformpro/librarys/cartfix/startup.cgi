my @cart = split(/\n/,$_ENV{'mfp_cart'});
my @cartenv = ();
for(my $i=0;$i<@cart;$i++){
	my ($name,$id,$price,$qty) = split(/\,/,$cart[$i]);
	1 while $price =~ s/(.*\d)(\d\d\d)/$1,$2/;
	push @cartenv,"${id}  ${name}  税込${price}  数量${qty}";
}
$_ENV{'mfp_cart'} = join("\n",@cartenv);
1;