## 設定ファイル
$config{"file.numticket.config"} = "$config{'data.dir'}numticket/config.cgi";

## jsonファイル
$config{"file.numticket.json"} = "$config{'data.dir'}numticket/numticket.json";

## update jsonファイル
$config{"file.numticket.update.json"} = "$config{'data.dir'}numticket/numticket.update.json";

## 識別子としてリストに残す情報（カンマ区切り）
$config{"file.numticket.value"} = 'お名前';

## ステータス用ファイル
$config{"file.numticket.status"} = "$config{'data.dir'}numticket/stat.cgi";

## 曜日別混雑ステータス
$config{"file.numticket.week.status"} = "$config{'data.dir'}numticket/week.cgi";

## 曜日別混雑ステータスjson
$config{"file.numticket.week.json"} = "$config{'data.dir'}numticket/week.json";

## 時間帯別混雑ステータス
$config{"file.numticket.hour.status"} = "$config{'data.dir'}numticket/hour.cgi";

## 時間帯別混雑ステータスjson
$config{"file.numticket.hour.json"} = "$config{'data.dir'}numticket/hour.json";

## 曜日・時間帯別待ち時間を集計するためのファイル
$config{"file.numticket.log"} = "$config{'data.dir'}numticket/log.cgi";

## 整理番号格納ファイル
$config{"file.numticket"} = "$config{'data.dir'}numticket/count.cgi";

## 整理番号リスト格納ファイル
$config{"file.numticket.list"} = "$config{'data.dir'}numticket/list.cgi";

## 整理券トークン保存ディレクトリ
$config{"dir.numticket.token"} = "$config{'data.dir'}numticket/token/";

## 管理機能にアクセスしづらくするための文字列
$config{"numticket.key"} = 'tnke7794RYHD';

## 番号重複を防ぐための接頭辞
$config{"numticket.prefix"} = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

## エラーメッセージ
$lang{'WarningNumticket'} = '現在、整理券の発行は行っていません。<br>No numbered tickets are being issued at this time.';

## ホスト名による管理を制限する場合は以下に指定してください。（複数の場合はカンマ区切り）
#$config{'numticket.HostName'} = 'localhost';

## IPアドレスによる管理を制限する場合は以下に指定してください。（複数の場合はカンマ区切り）
#$config{'numticket.IPAddress'} = '127.0.0.1';

## LINEステータス用ファイル
#$config{"LINE.file.numticket.status"} = "$config{'data.dir'}numticket/stat.line.cgi";

## LINE ログイン APIのチャンネルID
#$config{'LINE_LOGIN_client_id'} = '1654147468';

## LINE ログイン APIのチャンネルシークレット
#$config{'LINE_LOGIN_client_secret'} = '*******************************';

## LINE Messaging APIのチャンネルID
#$config{'LINE_MESSAGING_client_id'} = '**********';

## LINE Messaging APIのチャンネルID
#$config{'LINE_MESSAGING_client_secret'} = '*******************************';

## LINE Messaging APIのボットのベーシックID
#$config{'LINE_MESSAGING_basic_id'} = '@*******';

## LINE Messaging APIのチャネルアクセストークン（ロングターム）
#$config{'LINE_MESSAGING_access_token'} = '**********************************************************************************************************************************************************************************';

## LINE 通知メッセージのプリセットテキスト
#$config{'LINE_message_preset'} = 'あとすこしでお客様の順番になります。待合室までお越し下さい。';

## 以下、言語設定
$lang{'numticket.manager'} = '順番待ち受付状況管理';

sub _NUMTICKET_JSON {
	my($wait,$message,@numticket) = @_;
	my $qty = @numticket;
	my $time = (stat $config{"file.numticket.list"})[9];
	my $status = 'false';
	if(-f $config{"file.numticket.status"}){
		$status = 'true';
	}
	my @list = ();
	for(my $i=0;$i<@numticket;$i++){
		my ($num,$code,$hash,$time,$waitTime,$value) = split(/\t/,$numticket[$i]);
		my $parts = <<"		__HTML__";
			{
				num: '${num}',
				time: ${time},
				wait: ${waitTime}
			}
		__HTML__
		push @list,$parts;
	}
	my $list = join("\,",@list);
	my $json = <<"	__HTML__";
		numticket.action.callback.list({
			qty: ${qty},
			wait: ${wait},
			time: ${time},
			status: ${status},
			message: '${message}',
			list: [
				${list}
			]
		});
	__HTML__
	$json =~ s/\t//ig;
	$json =~ s/\n//ig;
	&_SAVE($config{"file.numticket.json"},$json);
	my $time = time;
	&_SAVE($config{"file.numticket.update.json"},"numticket.action.callback.update(${time});");
}
1;