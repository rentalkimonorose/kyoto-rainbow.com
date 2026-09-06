## 許可するURLのリストを改行区切りで
$config{'referercheck'} = <<'__URI__';
http://www.example.jp/contact/index.html
https://www.example.jp/contact/index.html
http://example.jp/contact/index.html
https://example.jp/contact/index.html
https://cgi.synck.com/mailformpro/mailformpro4.2.4/example.html
__URI__

$lang{'WarningRefererCheck'} = '送信元が確認できなかったため、メールを送信できませんでした。<br>We could not send mail because the sender could not be confirmed.';

1;