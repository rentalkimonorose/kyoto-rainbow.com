## Questionnaire config

## アンケート集計用ファイル
$config{'questionnaire2.file'} = "$config{'data.dir'}dat.questionnaire2.cgi";

## アンケート集計の表示を許可する
$config{'questionnaire2.result'} = 1;

## アンケート集計のjsonアクセスを許可する
$config{'questionnaire2.json'} = 1;

## 一度の送信で複数回のカウントを許可しない
$config{'questionnaire2.conflict'} = 1;

## 集計対象を格納する連想配列
%questionnaire2 = ();

## 集計対象のname属性をカンマ区切りで指定
## $questionnaire2{'集計する名称'} = '集計対象のname属性をカンマ区切りで指定';
$questionnaire2{'理事'} = '理事_選挙ID1,理事_選挙ID2,理事_選挙ID3,理事_選挙ID4';
$questionnaire2{'監事'} = '監事_選挙ID1,監事_選挙ID2,監事_選挙ID3,監事_選挙ID4';
1;