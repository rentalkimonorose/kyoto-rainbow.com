unshift @_ENV,'blacklist';
my $BlackListHash = &_HASH($ENV{'HTTP_HOST'} . "." . $ENV{'REMOTE_ADDR'});
$_ENV{'blacklist'} = "IP「$ENV{'REMOTE_ADDR'}」をブロックする場合、以下のURLにアクセスしてください。\n";
$_ENV{'blacklist'} .= &_URI2PRAM($config{'uri'},"module=blacklist&key=${BlackListHash}&ip=$ENV{'REMOTE_ADDR'}");
1;