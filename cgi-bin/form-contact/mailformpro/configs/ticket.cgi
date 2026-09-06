$config{'about'} = 'ticket Module';

## ticketデータディレクトリ
$config{'dir.ticket'} = "$config{'data.dir'}ticket/";

## tsvファイルの文字コード変換 （1：SJIS->UTF-8に変換、0：無変換）
## tsvファイルをUTF-8に変換するのが面倒な場合は有効にしてください
$config{'ticket.encode'} = 1;
1;