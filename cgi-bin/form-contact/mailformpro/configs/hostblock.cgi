## ブロックするホスト名のリストを改行区切りで指定してください。
## 後方一致のため例えばホスト名のトップレベルドメインが「br」（ブラジル）の場合、ブロックしたい！という際は
## .br
## と指定してください。
$config{'hostblock'} = <<'__URI__';
.br
.netvigator.com
.amazonaws.com
__URI__

$config{'hostblock_logfile'} = './data/hostblock.cgi';
$lang{'WarningHostnameCheck'} = 'ホスト名により送信が許可されませんでした。<br>Transmission was not allowed due to the hostname.';

1;