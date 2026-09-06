my @code = &_DB("./configs/coupon.tsv.cgi");
$_GET{'code'} =~ s/\|//ig;
$_GET{'code'} =~ s/\t//ig;
$_GET{'code'} =~ s/\n//ig;
$_GET{'code'} = &_SECURE($_GET{'code'});

@code = grep(/^$_GET{'code'}\t/,@code);
if(@code > 0){
	my @c = split(/\t/,$code[0]);
	my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
	my $date = sprintf("%04d-%02d-%02d",$year+1900,$mon+1,$day);
	if($c[1] le $date && $date le $c[2]){
		$js =  "callbackCouponCheck(false,\"${c[3]}\")\n";
	}
	else {
		$js =  "callbackCouponCheck(true,\"このクーポンコードは有効期限外のため、ご利用になれません。\")\n";
	}
}
else {
	$js =  "callbackCouponCheck(true,\"このクーポンコードはご利用になれません。\")\n";
}
1;