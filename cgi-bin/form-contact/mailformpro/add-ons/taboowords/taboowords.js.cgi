$_GET{'callback'} =~ s/[^0-9A-Za-z\.\_]//ig;
if($_GET{'callback'}){
	$js = "$_GET{'callback'}(\['" . join("','",@TabooWords) . "'\])";
}
1;