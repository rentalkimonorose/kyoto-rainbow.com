unshift @_ENV,'numticket.manager';
$_ENV{'numticket.manager'} = &_MFP2URI("module=numticket&key=$config{'numticket.key'}");
1;