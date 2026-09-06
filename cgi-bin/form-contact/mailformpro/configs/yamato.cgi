
## 加盟店コード
$config{'yamato.trader_code'} = '*********';

#$config{'yamato.Uri'} = 'https://payment.kuronekoyamato.co.jp/webcollect/settleSelectAction.gw';
$config{'yamato.Uri'} = 'https://ptwebcollect.jp/test_gateway/settleSelectAction.gw';
$config{'yamato.Token.dir'} = "$config{'data.dir'}yamato_token/";
$config{'yamato.expire'} = 1800;
$config{'yamato.PaymentType'} = '決済方法';
$config{'yamato.PaymentName'} = 'クレジット決済';
$config{'yamato.CancelPage'} = '../cancel.html';
$config{'yamato.NoticeFrom'} = 'no-reply@synck.com';

$_TEXT{'yamato_buyer_name_kanji'} = '<_姓_>　<_名_>';
$_TEXT{'yamato_buyer_name_kana'} = '<_セイ_>　<_メイ_>';
$_TEXT{'yamato_buyer_tel'} = '<_電話番号_>';
$_TEXT{'yamato_buyer_email'} = '<_email_>';

$_YAMATO_PAYMENT{'TRS_MAP'} = 'V_W02';
$_YAMATO_PAYMENT{'trader_code'} = $config{'yamato.trader_code'}; ## 加盟店コード
$_YAMATO_PAYMENT{'order_no'} = ''; ## 受付番号
$_YAMATO_PAYMENT{'goods_name'} = ''; ## 商品名称
$_YAMATO_PAYMENT{'settle_price'} = ''; ## 決済金額
$_YAMATO_PAYMENT{'buyer_name_kanji'} = ''; ## 購入者様漢字氏名
$_YAMATO_PAYMENT{'buyer_tel'} = ''; ## 購入者様電話番号
$_YAMATO_PAYMENT{'buyer_email'} = ''; ## 購入者様メールアドレス
$_YAMATO_PAYMENT{'buyer_name_kana'} = ''; ## 購入者様カナ氏名
$_YAMATO_PAYMENT{'return_url'} = ''; ## 決済結果データ自動送信ＵＲＬ
$_YAMATO_PAYMENT{'payment_method'} = ''; ## 決済手段
$_YAMATO_PAYMENT{'success_url'} = ''; ## 戻り先URL（正常時）
$_YAMATO_PAYMENT{'failure_url'} = ''; ## 戻り先URL（異常時）
$_YAMATO_PAYMENT{'cancel_url'} = ''; ## 戻り先URL（キャンセル時）
1;