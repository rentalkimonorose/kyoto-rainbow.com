## memory config

## 記憶ファイルを格納するディレクトリ
$config{'dir.memory'} = "$config{'data.dir'}memory/";

## 記憶対象のエレメント名（カンマ区切り）
$config{'memory.element.name'} = '姓,名,セイ,メイ,email';

## 保存を許可する場合のエレメント名
$config{'memory.accept.element.name'} = '入力内容を記録';

## 任意パスワードのエレメント名 (任意パスワードを許可する場合はコメントを解除
## パスワードが入力されていない場合は保存されません
#$config{'memory.password.element.name'} = 'パスワード';

## パスワード自動発行時の桁数
$config{'memory.passcode.digit'} = 5;

1;