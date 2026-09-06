unshift @_ENV,'ReplyTime';
$ReplyTimeHash = &_HASH(time . "." . $ENV{'REMOTE_ADDR'} . $_ENV{'mfp_serial'});
$_ENV{'ReplyTime'} = "返信が完了後に以下のURLにアクセスしてください。\n";
$_ENV{'ReplyTime'} .= &_MFP2URI("module=ReplyTime&key=${ReplyTimeHash}");
1;