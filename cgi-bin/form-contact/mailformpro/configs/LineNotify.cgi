## アクセストークン
## 01.LINE Notifyにアクセスする
## https://notify-bot.line.me/
## 02.マイページからトークンを発行する
## 発行されたトークンを以下にコピーしてください。
$config{'LineNotify.AccessToken'} = '*********************************************';

## メッセージ内容
$_TEXT{'LineNotify.Message'} = <<'__HTML__';
お問い合わせメールフォームに <_お名前_> 様からメールが届きました。
__HTML__
1;