if($_GET{'key'} ne $null && $_GET{'ip'} ne $null){
	my $BlackListHash = &_HASH($ENV{'HTTP_HOST'} . "." . $_GET{'ip'});
	if($_GET{'key'} eq $BlackListHash && !($_GET{'ip'} =~ /[^0-9\.]/)){
		my $path = "$config{'blacklist.dir'}$_GET{'ip'}.cgi";
		&_SAVE($path,time);
		my $parts = <<"		__HTML__";
			<table>
				<tr>
					<td>Registed $_GET{'ip'}</td>
				</tr>
			</table>
		__HTML__
		$html = &_LOAD("./librarys/blacklist/download.tpl");
		$html =~ s/_%%content%%_/$parts/ig;
		print "Pragma: no-cache\n";
		print "Cache-Control: no-cache\n";
		print "Content-type: text/html; charset=UTF-8\n\n";
		print $html;
	}
	else {
		&_Error(0);
	}
}
else {
	&_Error(0);
}
exit;