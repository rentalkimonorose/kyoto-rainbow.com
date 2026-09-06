## トークンを記録するディレクトリ
$config{"onetimetoken.dir"} = "$config{'data.dir'}onetimetoken/";

## トークンのキー（なんでもよい）
$config{"onetimetoken.key"} = '0123456789';

## エラーメッセージ
$lang{'WarningOnetimeToken'} = 'トークンの有効期限が切れています。<br>The token has expired.';

## トークンの有効期限
$config{"onetimetoken.exp"} = 3600;
1;