$_GET{'zip'} =~ s/[^0-9]//ig;
if($_GET{'zip'} ne $null){
	$path = sprintf("$config{'dir.AddOns'}/prefcode/%02d.cgi",substr($_GET{'zip'},0,2));
	if(-f $path){
		@zip = &_DB($path);
		@zip = grep(/^$_GET{'zip'}/,@zip);
		if(@zip > 0){
			@zip = split(/\,/,$zip[0]);
			$_GET{'a1'} = &_SANITIZING($_GET{'a1'});
			$_GET{'a2'} = &_SANITIZING($_GET{'a2'});
			$_GET{'a3'} = &_SANITIZING($_GET{'a3'});
			$js =  "callbackMFPZip(true,\"$_GET{'a1'}\",\"$_GET{'a2'}\",\"$_GET{'a3'}\",\"${zip[1]}\",\"${zip[2]}\",\"${zip[3]}\")\n";
		}
	}
}
