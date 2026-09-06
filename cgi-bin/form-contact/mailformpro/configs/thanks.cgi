$config{'about'} = 'Thanks Module';

## パラメータ保存の有効期限(秒数)
$config{'thanks.expire'} = 10;

## 取得可能ホスト(サンクスページのドメイン)
## 前方一致でチェックするため、プロトコルから指定してください
$config{'thanks.domain'} = $config{'protocol'} . $ENV{'HTTP_HOST'};

## 環境変数を含める(1:ON / 0:OFF)
$config{'thanks.env'} = 1;

## 環境変数のハッシュを日本語にする(1:ON / 0:OFF)
$config{'thanks.env.jp'} = 0;
1;