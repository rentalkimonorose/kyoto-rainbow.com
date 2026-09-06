&_POST;
my $html = &_LOAD("./librarys/numticket/template.tpl");
my($sec,$min,$hour,$day,$mon,$year) = localtime(time);
my %_HTML = ();
my @section = ();
my @result = ();
my $err = 0;
my $jsonp = "";
my $redirect = "";

sub _COUNTUP {
	my($path) = @_;
	open(FH,">>${path}");
		print FH '0';
	close(FH);
}
sub _MIN {
	my($min) = @_;
	if($min > 0){
		$min = int($min / 60);
		return "${min}分";
	}
	else {
		return "0分";
	}
}
sub _LINE_REQUEST_ACCESS_TOKEN {
	my ($code) = @_;
	my $ua = LWP::UserAgent->new;
	my $uri = 'https://api.line.me/oauth2/v2.1/token';
	my %_LINE_POST = ();
	$_LINE_POST{'grant_type'} = 'authorization_code';
	$_LINE_POST{'code'} = $code;
	$_LINE_POST{'redirect_uri'} = &_MFP2URI("module=numticket");
	$_LINE_POST{'client_id'} = $config{'LINE_LOGIN_client_id'};
	$_LINE_POST{'client_secret'} = $config{'LINE_LOGIN_client_secret'};
	my $req  = POST($uri, [%_LINE_POST]);
	my $res = $ua->request($req);
	my $doc = $res->content;
	if($doc =~ /\"access_token\"\:\"(.*?)\"/){
		$_LINE_INIT{'access_token'} = $1;
	}
	if($doc =~ /\"refresh_token\"\:\"(.*?)\"/){
		$_LINE_INIT{'refresh_token'} = $1;
	}
}
sub _LINE_REQUEST_PROFILE {
	my $ua = LWP::UserAgent->new;
	$ua->default_header('Authorization' => "Bearer $_LINE_INIT{'access_token'}");
	my $uri = "https://api.line.me/v2/profile";
	my $req = HTTP::Request->new(GET => $uri);
	$req->referer($url);
	my $res = $ua->request($req);
	my $doc = $res->content;
	if($doc =~ /\"userId\"\:\"(.*?)\"/){
		$_LINE_INIT{'userId'} = $1;
	}
	if($doc =~ /\"displayName\"\:\"(.*?)\"/){
		$_LINE_INIT{'displayName'} = $1;
	}
	if($doc =~ /\"pictureUrl\"\:\"(.*?)\"/){
		$_LINE_INIT{'pictureUrl'} = $1;
	}
}
sub _LINE_REQUEST_CHANEL_PUSH_MESSAGE {
	my($to,$text) = @_;
	my $ua = LWP::UserAgent->new;
	$ua->default_header('Authorization' => "Bearer $config{'LINE_MESSAGING_access_token'}");
	$ua->default_header('Content-Type' => "application/json");
	my $uri = 'https://api.line.me/v2/bot/message/push';
my $json = <<__POST_JSON__;
\{
    "to"\: "${to}",
    "messages"\:\[
        \{
            "type"\:"text",
            "text"\:"${text}"
        \}
    \]
\}
__POST_JSON__
	my $req= HTTP::Request->new(POST => $uri);
	$req->content($json);
	my $result = $ua->request($req)->as_string;
	#&_SAVE("./_04_request_channel_push_message.json",$json);
	#&_SAVE("./_04_request_channel_push_message.txt",$ua->request($req)->as_string);
}

## config
## [0] encrypt password
## [1] min
## [2] コメント
$_HTML{'time'} = time;
$_HTML{'json'} = $config{"file.numticket.json"};
$_HTML{'update'} = $config{"file.numticket.update.json"};
if($_GET{'state'}){
	my $token = $config{"dir.numticket.token"} . &_SECPATH($_GET{'state'}) . '.cgi';
	my $linetoken = $config{"dir.numticket.token"} . &_SECPATH($_GET{'state'}) . '.line.cgi';
	if(-f $token){
		## アクセストークンの取得
		use Encode;
		use LWP::UserAgent;
		use HTTP::Request::Common qw(POST);
		use HTTP::Request;
		&_LINE_REQUEST_ACCESS_TOKEN($_GET{'code'});
		if($_LINE_INIT{'access_token'}){
			&_LINE_REQUEST_PROFILE;
			if($_LINE_INIT{'userId'}){
				my @data = ($_LINE_INIT{'access_token'},$_LINE_INIT{'refresh_token'},$_LINE_INIT{'userId'},$_LINE_INIT{'displayName'},$_LINE_INIT{'pictureUrl'});
				&_SAVE($linetoken,join("\n",@data));
				$redirect = &_MFP2URI("module=numticket&token=$_GET{'state'}");
			}
			else {
				&_Error(1);
				$err = 1;
			}
		}
		else {
			&_Error(2);
			$err = 1;
		}
	}
	else {
		&_Error(3);
		$err = 1;
	}
}
elsif($_GET{'json'}){
	if($_GET{'traffic'}){
		my $week = "null";
		my $hour = "null";
		my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
		if(-f $config{"file.numticket.week.status"} && -f $config{"file.numticket.week.status"}){
			$week = &_LOAD($config{"file.numticket.week.json"});
		}
		if(-f "$config{'file.numticket.hour.json'}.w${wday}.json" && -f $config{"file.numticket.hour.status"}){
			$hour = &_LOAD("$config{'file.numticket.hour.json'}.w${wday}.json");
		}
		$jsonp = "numticket.action.traffic(${week},${hour});";
	}
	else {
		$jsonp = &_LOAD($config{"file.numticket.json"});
	}
}
elsif($_GET{'key'} eq $config{"numticket.key"}){
	## administrator
	my $hostname = &_GETHOST;
	my $check = 0;
	my $qrcode = &encodeURI(&_MFP2URI("module=numticket&key=$_GET{'key'}"));
	
	## Host check
	if($config{'numticket.HostName'}){
		my @hostname = split(/\,/,$config{'numticket.HostName'});
		if(grep(/^${hostname}$/,@hostname) < 1){
			$check = 1;
		}
	}
	
	## IP Address check
	if($config{'numticket.IPAddress'}){
		my @ipadd = split(/\,/,$config{'numticket.IPAddress'});
		if(grep(/^$ENV{'REMOTE_ADDR'}$/,@ipadd) < 1){
			$check = 1;
		}
	}
	
	if(!$check){
		if(-f $config{"file.numticket.config"}){
			## auth
			my @config = &_DB($config{"file.numticket.config"});
			my $passwd = $_POST{'passwdc'};
			if($_POST{'passwd'}){
				$passwd = &_HASH($_POST{'passwd'});
			}
			if($config[0] eq $passwd){
				my $lineFeature = 0;
				$_HTML{'title'} = '整理番号発行管理画面';
				my @numticket = &_DB($config{"file.numticket.list"});
				## Auth ok
				my $pw = "<input type=\"hidden\" name=\"passwdc\" value=\"${passwd}\">";
				if($_POST{'min'} || $_POST{'message'}){
					$config[1] = $_POST{'min'};
					$config[2] = &_SANITIZING($_POST{'message'});
					&_SAVE($config{"file.numticket.config"},join("\n",@config));
					$_HTML{'status'} = '<div id="status">保存が完了しました</div>';
					&_NUMTICKET_JSON($config[1],$config[2],@numticket);
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">保存が完了しました</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'line' && $_POST{'line_hash'} && $_POST{'line_num'} && $_POST{'line_message'}){
					my $lineToken = "$config{'dir.numticket.token'}$_POST{'line_hash'}.line.cgi";
					if(-f $lineToken){
						my @line = &_DB($lineToken);
						use Encode;
						use LWP::UserAgent;
						use HTTP::Request::Common qw(POST);
						use HTTP::Request;
						&_LINE_REQUEST_CHANEL_PUSH_MESSAGE($line[2],&_SANITIZING($_POST{'line_message'}));
						my $lineTokenCount = "$config{'dir.numticket.token'}$_POST{'line_hash'}.line.count.cgi";
						&_COUNTUP($lineTokenCount);
					}
					$_HTML{'status'} = "<div id=\"status\">$_POST{'line_num'}に通知しました</div>";
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">$_POST{'line_num'}に通知しました</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'switch'){
					my $statName = '無効にしました';
					if(-f $config{"file.numticket.status"}){
						unlink $config{"file.numticket.status"};
						$_HTML{'status'} = '<div id="status">無効しました</div>';
					}
					else {
						&_SAVE($config{"file.numticket.status"},$null);
						$_HTML{'status'} = '<div id="status">有効しました</div>';
						$statName = '有効にしました';
					}
					&_NUMTICKET_JSON($config[1],$config[2],@numticket);
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">${statName}</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'week'){
					my $statName = '無効にしました';
					if(-f $config{"file.numticket.week.status"}){
						unlink $config{"file.numticket.week.status"};
						$_HTML{'status'} = '<div id="status">無効しました</div>';
					}
					else {
						&_SAVE($config{"file.numticket.week.status"},$null);
						$_HTML{'status'} = '<div id="status">有効しました</div>';
						$statName = '有効にしました';
					}
					&_NUMTICKET_JSON($config[1],$config[2],@numticket);
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">${statName}</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'hour'){
					my $statName = '無効にしました';
					if(-f $config{"file.numticket.hour.status"}){
						unlink $config{"file.numticket.hour.status"};
						$_HTML{'status'} = '<div id="status">無効しました</div>';
					}
					else {
						&_SAVE($config{"file.numticket.hour.status"},$null);
						$_HTML{'status'} = '<div id="status">有効しました</div>';
						$statName = '有効にしました';
					}
					&_NUMTICKET_JSON($config[1],$config[2],@numticket);
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">${statName}</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'lineswitch'){
					my $statName = 'LINE通知機能を無効にしました';
					if(-f $config{'LINE.file.numticket.status'}){
						unlink $config{'LINE.file.numticket.status'};
						$_HTML{'status'} = '<div id="status">無効しました</div>';
					}
					else {
						&_SAVE($config{'LINE.file.numticket.status'},$null);
						$_HTML{'status'} = '<div id="status">有効しました</div>';
						$statName = 'LINE通知機能を有効にしました';
					}
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">${statName}</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'remove' && $_POST{'hash'} ne $null){
					unlink "$config{'dir.numticket.token'}$_POST{'hash'}.cgi";
					unlink "$config{'dir.numticket.token'}$_POST{'hash'}.line.cgi";
					unlink "$config{'dir.numticket.token'}$_POST{'hash'}.line.count.cgi";
					@numticket = grep(!/\t$_POST{'hash'}\t/,@numticket);
					&_SAVE($config{"file.numticket.list"},join("\n",@numticket));
					$_HTML{'status'} = '<div id="status">取り消しました</div>';
					&_NUMTICKET_JSON($config[1],$config[2],@numticket);
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">取り消しました</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'finish' && $_POST{'hash'} ne $null){
					unlink "$config{'dir.numticket.token'}$_POST{'hash'}.cgi";
					unlink "$config{'dir.numticket.token'}$_POST{'hash'}.line.cgi";
					unlink "$config{'dir.numticket.token'}$_POST{'hash'}.line.count.cgi";
					my @data = split(/\t/,(grep(/\t$_POST{'hash'}\t/,@numticket))[0]);
					@numticket = grep(!/\t$_POST{'hash'}\t/,@numticket);
					&_SAVE($config{"file.numticket.list"},join("\n",@numticket));
					
					## Log
					## Week
					## Wait time
					## Hour
					## ($numticket,$passwd,$hash,$time,($waitTime*60*($qty+1)),join("<br />",@value));
					my $t = time;
					my $wait = $t - $data[3];
					my $precision = $t - ($data[3] + $data[4]);
					my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
					my $lday = sprintf("%04d-%02d-%02d",$year+1900,$mon+1,$mday);
					my @hash = ("w${wday}-${hour}","w${wday}","h${hour}");
					my @nlog = &_DB($config{"file.numticket.log"});
					for(my $i=0;$i<@hash;$i++){
						my ($key,$qty,$time,$avg,$preci) = split(/\t/,(grep(/^${hash[$i]}\t/,@nlog))[0]);
						@nlog = grep(!/^${hash[$i]}\t/,@nlog);
						$key = $hash[$i];
						$qty++;
						$time += $wait;
						$avg = int($time / $qty);
						$preci += $precision;
						my @log = ($key,$qty,$time,$avg,$preci);
						push @nlog,join("\t",@log);
					}
					&_SAVE($config{"file.numticket.log"},join("\n",@nlog));
					##
					
					## Rebuild json
					my @jsonWeek = ();
					for(my $i=0;$i<7;$i++){
						my ($key,$qty,$time,$avg,$wait) = split(/\t/,(grep(/^w${i}\t/,@nlog))[0]);
						if($avg > 0){
							push @jsonWeek,$avg;
						}
						else {
							push @jsonWeek,0;
						}
						my @jsonHour = ();
						for(my $ii=0;$ii<24;$ii++){
							my @t = split(/\t/,(grep(/^w${i}-${ii}\t/,@nlog))[0]);
							if($t[3] > 0){
								push @jsonHour,$t[3];
							}
							else {
								push @jsonHour,0;
							}
						}
						my $jsonHour = join("\,",@jsonHour);
						&_SAVE("$config{'file.numticket.hour.json'}.w${i}.json","\[${jsonHour}\]");
					}
					my $jsonWeek = join("\,",@jsonWeek);
					&_SAVE($config{"file.numticket.week.json"},"\[${jsonWeek}\]");
					##
					
					$_HTML{'status'} = '<div id="status">完了しました</div>';
					&_NUMTICKET_JSON($config[1],$config[2],@numticket);
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">完了しました</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'reset'){
					$_HTML{'status'} = '<div id="status">リセットしました</div>';
					&_SAVE($config{"file.numticket"},0);
					&_SAVE($config{"file.numticket.list"},$null);
					@numticket = ();
					&_NUMTICKET_JSON($config[1],$config[2],@numticket);
					my $cd = $config{"dir.numticket.token"};
					my @dirs = ($cd);
					while(@dirs > 0){
						$dir = shift @dirs;
						opendir DH, $dir;
						while (my $file = readdir DH) {
							next if $file =~ /^\.{1,2}$/;
							my $path = "${dir}${file}";
							if(!(-d $path)){
								my @file = split(/\./,$file);
								my $type = lc (pop @file);
								my $name = join('.',@file);
								if($type eq 'cgi'){
									unlink $path;
								}
							}
						}
						closedir DH;
					}
					my $parts = <<"					__HTML__";
						<section>
							<p class="result">リセットしました</p>
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$parts;
				}
				elsif($_POST{'method'} eq 'add'){
					## add number
					my $count = &_LOAD($config{"file.numticket"});
					$count++;
					&_SAVE($config{"file.numticket"},$count);
					
					my @prefix = split(//,$config{"numticket.prefix"});
					my $prefix = @prefix;
					my $index = int(rand() * (@prefix));
					$prefix = $prefix[$index];
					my $numticket = sprintf("${prefix}%04d",$count);
					my $hash = &_HASH(time . $ENV{'REMOTE_ADDR'} . $count);
					
					my $digit = 4;
					my $passwd = "";
					for(my $i=0;$i<$digit;$i++){
						$passwd .= int(rand() * 10);
					}
					my $time = time;
					my $waitTime = $config[1] || 10;
					my $qty = @numticket;
					
					my @data = ($numticket,$passwd,$hash,$time,($waitTime*60*($qty+1)),&_SANITIZING($_POST{'name'}));
					push @numticket,join("\t",@data);
					my $data = "\n" . join("\t",@data);
					&_ADDSAVE($config{"file.numticket.list"},$data);
					&_NUMTICKET_JSON($config[1],$config[2],@numticket);
					
					## Token create
					my @token = ($numticket,$passwd,$time);
					&_SAVE("$config{'dir.numticket.token'}${hash}.cgi",join("\n",@token));
					my $href = &encodeURI(&_MFP2URI("module=numticket&token=${hash}"));
					
					$_HTML{'status'} = '<div id="status">発行しました</div>';
					my $section = <<"					__HTML__";
						<section>
							<p class="result">整理番号を発行しました</p>
							<h2>発行された整理番号</h2>
							<table class="ticket">
								<thead>
									<tr>
										<th>整理番号</th>
										<td>${numticket}</td>
									</tr>
								</thead>
								<tbody>
									<tr>
										<th>照会番号</th>
										<td>${passwd}</td>
									</tr>
								</tbody>
							</table>
							<img src="https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=${href}">
							<form method="post">
								${pw}
								<div class="button">
									<button>戻る</button>
								</div>
							</form>
						</section>
					__HTML__
					push @result,$section;
				}
				
				## Dashboard
				
				## Reload
				my $section = <<"				__HTML__";
					<form method="post" id="reload">${pw}
							<button id="reload_button"><img src="data:image/png;base64,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"></button>
					</form>
				__HTML__
				push @section,$section;
				
				## Switch
				my $toggleStatus = '<strong style="color: #900;">無効</strong>';
				my $toggleLabel = '有効';
				if(-f $config{"file.numticket.status"}){
					$toggleStatus = '<strong style="color: #090;">有効</strong>';
					$toggleLabel = '無効';
				}
				my $section = <<"				__HTML__";
					<section>
						<h2>現在の受付状態：${toggleStatus}</h2>
						<form method="post" onsubmit="return confirm('受付を${toggleLabel}にしてよろしいですか？')">${pw}
							<input type="hidden" name="method" value="switch">
							<div class="button">
								<button>受付を${toggleLabel}にする</button>
							</div>
						</form>
					</section>
				__HTML__
				push @section,$section;
				
				
				## List
				if(@numticket > 0){
					my $qty = @numticket;
					my @tr = ();
					my $now = time;
					for(my $i=0;$i<@numticket;$i++){
						my $index = $i + 1;
						my $className = $i % 2;
						my ($num,$code,$hash,$time,$waitTime,$value) = split(/\t/,$numticket[$i]);
						
						my $lineToken = "$config{'dir.numticket.token'}${hash}.line.cgi";
						
						my $min = &_MIN($now-$time);
						my $wait = &_MIN($config[1]*60 * ($i+1));
						my($sec,$mi,$hour,$day,$mon,$year) = localtime($time+$config[1]*60 * ($i+1));
						my $calcHour = sprintf("%02d:%02d",$hour,$mi);
						
						my($sec,$mi,$hour,$day,$mon,$year) = localtime($time+$waitTime);
						my $calcTime= sprintf("%02d:%02d",$hour,$mi);
						
						if($value eq $null){
							$value = '情報なし。';
						}
						
						my $lineStatus = "";
						my $lineAction = " disabled=\"disabled\"";
						my $linecount = "";
						if(-f $lineToken){
							$lineStatus = " active";
							$lineAction = " data-hash=\"${hash}\" data-num=\"${num}\" class=\"line_button\"";
							$lineFeature = 1;
							my $size = -s "$config{'dir.numticket.token'}${hash}.line.count.cgi";
							if($size > 0){
								$linecount = "<span>${size}</span>";
							}
						}
						my $tr = <<"						__HTML__";
							<tr class="tr${className}">
								<td>${index}</td>
								<th onclick="show('tr_${i}')">${num}</th>
								<td>${code}</td>
								<td>${wait} / ${calcHour}</td>
								<td>${calcTime}</td>
								<td>${min}前</td>
								<td class="line${lineStatus}">${linecount}
									<button type="button"${lineAction}><div class="line_icon"></div></button>
								</td>
								<td>
									<form method="post" onsubmit="return confirm('完了処理をしてもよいですか？')">${pw}
										<input type="hidden" name="method" value="finish">
										<input type="hidden" name="hash" value="${hash}">
										<button>完了</button>
									</form>
								</td>
								<td>
									<form method="post" onsubmit="return confirm('キャンセル処理をしてもよいですか？')">${pw}
										<input type="hidden" name="method" value="remove">
										<input type="hidden" name="hash" value="${hash}">
										<button>取消</button>
									</form>
								</td>
							</tr>
							<tr class="tr${className}" id="tr_${i}" style="display: none;">
								<td colspan="9"><div>${value}</div></td>
							</tr>
						__HTML__
						push @tr,$tr;
					}
					my $tr = join("\n",@tr);
					my $section = <<"					__HTML__";
						<section>
							<h2>整理番号発行状況</h2>
							<p>現在、<strong>${qty}</strong>件の整理番号が発行されています。</p>
							<table class="list">
								<thead>
									<tr>
										<th>順番</th>
										<th>整理番号</th>
										<th>照会番号</th>
										<th>待時間目安</th>
										<th>予測時間</th>
										<th>発行時間</th>
										<th>LINE</th>
										<th>完了</th>
										<th>取消</th>
									</tr>
								</thead>
								<tbody>
									${tr}
								</tbody>
							</table>
						</section>
					__HTML__
					push @section,$section;
					if($lineFeature){
						my $section = <<"						__HTML__";
							<section id="line_message_wrapper">
								<h2>LINEでメッセージを通知</h2>
								<form method="post">${pw}
									<input type="hidden" name="method" value="line">
									<input type="hidden" name="line_hash" id="line_hash">
									<dl>
										<dt>通知相手</dt>
										<dd><input type="text" name="line_num" id="line_num" readonly="readonly"></dd>
										
										<dt>メッセージ内容</dt>
										<dd><textarea name="line_message" id="line_message" rows="2">$config{'LINE_message_preset'}</textarea></dd>
									</dl>
									<div class="button">
										<button>LINEに通知する</button>
									</div>
								</form>
							</section>
						__HTML__
						push @section,$section;
					}
				}
				else {
					my $section = <<"					__HTML__";
						<section>
							<h2>整理番号発行状況</h2>
							<p>現在、待機中の番号はありません。</p>
						</section>
					__HTML__
					push @section,$section;
				}
				
				## add
				my $section = <<"				__HTML__";
					<section>
						<h2>手動発行</h2>
						<form method="post">${pw}
							<input type="hidden" name="method" value="add">
							<dl>
								<dt>お名前等、識別子</dt>
								<dd><textarea name="name" placeholder="お名前やID等、識別できる文字列を入力してください" rows="3"></textarea></dd>
							</dl>
							<div class="button">
								<button>発行</button>
							</div>
						</form>
					</section>
				__HTML__
				push @section,$section;
				
				## Setting
				$config[2] = &_UNSANITIZING($config[2]);
				my $section = <<"				__HTML__";
					<section>
						<h2>基本設定</h2>
						<form method="post">${pw}
							<dl>
								<dt>1件あたりに係る時間（分）</dt>
								<dd><input type="number" name="min" value="${config[1]}"></dd>
								<dt>受付画面に表示するメッセージ</dt>
								<dd><textarea name="message" rows="10">${config[2]}</textarea></dd>
							</dl>
							<div class="button">
								<button>保存</button>
							</div>
						</form>
					</section>
				__HTML__
				push @section,$section;
				
				if($config{'LINE_LOGIN_client_id'}){
					## Switch
					my $toggleStatus = '<strong style="color: #900;">無効</strong>';
					my $toggleLabel = '有効';
					if(-f $config{"LINE.file.numticket.status"}){
						$toggleStatus = '<strong style="color: #090;">有効</strong>';
						$toggleLabel = '無効';
					}
					my $section = <<"					__HTML__";
						<section>
							<h2>現在のLINE通知機能：${toggleStatus}</h2>
							<form method="post" onsubmit="return confirm('LINE通知機能を${toggleLabel}にしてよろしいですか？')">${pw}
								<input type="hidden" name="method" value="lineswitch">
								<div class="button">
									<button>LINE通知機能を${toggleLabel}にする</button>
								</div>
							</form>
						</section>
					__HTML__
					push @section,$section;
				}
				
				## 曜日別混雑ステータス
				my $toggleStatus = '<strong style="color: #900;">非表示</strong>';
				my $toggleLabel = '表示';
				if(-f $config{"file.numticket.week.status"}){
					$toggleStatus = '<strong style="color: #090;">表示</strong>';
					$toggleLabel = '非表示';
				}
				my $section = <<"				__HTML__";
					<section>
						<h2>曜日別混雑ステータス：${toggleStatus}</h2>
						<form method="post" onsubmit="return confirm('曜日別混雑ステータスを${toggleLabel}にしてよろしいですか？')">${pw}
							<input type="hidden" name="method" value="week">
							<div class="button">
								<button>曜日別混雑ステータスを${toggleLabel}にする</button>
							</div>
						</form>
					</section>
				__HTML__
				push @section,$section;
				
				## 時間帯別混雑ステータス
				my $toggleStatus = '<strong style="color: #900;">非表示</strong>';
				my $toggleLabel = '表示';
				if(-f $config{"file.numticket.hour.status"}){
					$toggleStatus = '<strong style="color: #090;">表示</strong>';
					$toggleLabel = '非表示';
				}
				my $section = <<"				__HTML__";
					<section>
						<h2>時間帯別混雑ステータス：${toggleStatus}</h2>
						<form method="post" onsubmit="return confirm('時間帯別混雑ステータスを${toggleLabel}にしてよろしいですか？')">${pw}
							<input type="hidden" name="method" value="hour">
							<div class="button">
								<button>時間帯別混雑ステータスを${toggleLabel}にする</button>
							</div>
						</form>
					</section>
				__HTML__
				push @section,$section;
				
				## Reset
				my $section = <<"				__HTML__";
					<section>
						<form method="post" onsubmit="return confirm('カウンタと登録内容をリセットしてもよろしいですか？')">
							${pw}
							<input type="hidden" name="method" value="reset">
							<div class="button">
								<button>カウンタと登録内容をリセット</button>
							</div>
						</form>
					</section>
				__HTML__
				push @section,$section;
				
				if(!($ENV{'HTTP_USER_AGENT'} =~ /mobile/sig)){
					my $section = <<"					__HTML__";
						<section>
							<h2>管理画面にスマートフォンからアクセスする</h2>
							<img src="https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=${qrcode}">
						</section>
					__HTML__
					push @section,$section;
				}
				
				## Logout
				my $section = <<"				__HTML__";
					<section>
						<form method="post">
							<div class="button">
								<button>ログアウト</button>
							</div>
						</form>
					</section>
				__HTML__
				push @section,$section;
				
			}
			else {
				$_HTML{'title'} = '整理番号発行管理ログイン画面';
				## Login screen
				my $section = <<"				__HTML__";
					<section>
						<form method="post">
							<dl>
								<dt>ログインパスワード</dt>
								<dd><input type="password" name="passwd" placeholder=""></dd>
								
							</dl>
							<div class="button">
								<button>ログイン</button>
							</div>
						</form>
					</section>
					<section>
						<img src="https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=${qrcode}">
					</section>
				__HTML__
				push @section,$section;
			}
		}
		else {
			if($_POST{'passwd'}){
				## setup
				my @data = (&_HASH($_POST{'passwd'}),10,"");
				&_SAVE($config{"file.numticket.config"},join("\n",@data));
				my $section = <<"				__HTML__";
					<section>
						<p>セットアップが完了しました。<a href="?module=numticket&key=$config{'numticket.key'}&type=$_GET{'type'}">ログイン画面</a>からログインしてください。</p>
					</section>
				__HTML__
				push @section,$section;
			}
			else {
				## setup
				my $section = <<"				__HTML__";
					<section>
						<form method="post">
							<dl>
								<dt>設定するパスワード</dt>
								<dd><input type="password" name="passwd" placeholder="設定するパスワードを入力してください"></dd>
								
							</dl>
							<div class="button">
								<button>初期設定を実行する</button>
							</div>
						</form>
					</section>
				__HTML__
				push @section,$section;
			}
		}
	}
	else {
		&_Error(0);
		$err = 1;
	}
}
elsif($_GET{'key'}){
	&_Error(0);
	$err = 1;
}
else {
	## Number Ticket screen
	$_HTML{'title'} = '整理番号確認画面';
	my @config = &_DB($config{"file.numticket.config"});
	my @numticket = &_DB($config{"file.numticket.list"});
	if($_GET{'token'}){
		$_GET{'token'} = &_SECPATH($_GET{'token'});
		if($_POST{'method'} eq 'remove'){
			$_POST{'token'} = &_SECPATH($_POST{'token'});
			my $token = $config{"dir.numticket.token"} . $_POST{'token'} . '.cgi';
			if(-f $token){
				unlink $token;
				unlink "$config{'dir.numticket.token'}$_POST{'token'}.line.cgi";
				unlink "$config{'dir.numticket.token'}$_POST{'token'}.line.count.cgi";
				@numticket = grep(!/\t$_POST{'token'}\t/,@numticket);
				&_SAVE($config{"file.numticket.list"},join("\n",@numticket));
				&_NUMTICKET_JSON($config[1],$config[2],@numticket);
			}
		}
		my $token = $config{"dir.numticket.token"} . &_SECPATH($_GET{'token'}) . '.cgi';
		## User screen
		if(-f $token){
			my @data = &_DB($token);
			my $index = 0;
			my $qty = @numticket;
			for(my $i=0;$i<@numticket;$i++){
				my ($num,$code,$hash,$time,$waitTime,$value) = split(/\t/,$numticket[$i]);
				if($hash eq $_GET{'token'}){
					$index = $i+1;
				}
			}
			my $msgstyle = '';
			if(!$config[2]){
				$msgstyle = ' style="display: none;"';
			}
			my $section = <<"			__HTML__";
				<section id="message_wrapper"${msgstyle}>
					<p id="message_inner">${config[2]}</p>
				</section>
			__HTML__
			push @section,$section;
			my $href = &encodeURI(&_MFP2URI("module=numticket&token=$_GET{'token'}"));
			my $min = &_MIN(($config[1]*60)*$index);
			my $section = <<"			__HTML__";
				<form method="post" id="reload">
					<button id="reload_button"><img src="data:image/png;base64,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"></button>
				</form>
				<section class="ticket">
					<p>お客様の整理番号<strong id="html_numticket">${data[0]}</strong></p>
					<p class="center">（照会番号：${data[1]}）</p>
				</section>
				<section class="ticket">
					<p>予想される待ち時間<strong id="html_waitTime">${min}</strong></p>
					<p class="center">（<span id="html_total_index">${qty}</span>人中<span id="html_index">${index}</span>人目です）</p>
				</section>
			__HTML__
			push @section,$section;
			
			my $lineToken = "$config{'dir.numticket.token'}$_GET{'token'}.line.cgi";
			if(-f $lineToken && -f $config{"LINE.file.numticket.status"}){
				my $id = &encodeURI($config{'LINE_MESSAGING_basic_id'});
				my $parts = <<"				__HTML__";
					<section>
						<h2>LINEで通知を受け取れるように登録してください</h2>
						<p>LINEに友だち登録をしていない場合は以下のQRコードから、または<a href="https://line.me/R/ti/p/${id}">このリンクから</a>登録してください。</a></p>
						<img src="https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=https://line.me/R/ti/p/${id}">
					</section>
				__HTML__
				push @section,$parts;
			}
			elsif($config{'LINE_MESSAGING_basic_id'} && -f $config{"LINE.file.numticket.status"}){
				## Login
				my $uri = &_MFP2URI("module=numticket");
				my $parts = <<"				__HTML__";
					<section>
						<h2>LINEで順番が来た際に通知を受け取る</h2>
						<form action="https://access.line.me/oauth2/v2.1/authorize">
							<input type="hidden" name="response_type" value="code">
							<input type="hidden" name="client_id" value="$config{'LINE_LOGIN_client_id'}">
							<input type="hidden" name="redirect_uri" value="${uri}">
							<input type="hidden" name="state" value="$_GET{'token'}">
							<input type="hidden" name="scope" value="profile">
							<input type="hidden" name="bot_prompt" value="aggressive">
							<button style="border: none;background: none;">
								<img style="margin: 10px auto;max-width: 160px;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAS8AAABYCAYAAACkjnEVAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA3NpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDIxIDc5LjE1NDkxMSwgMjAxMy8xMC8yOS0xMTo0NzoxNiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDphNTk0YTczYS0zNzEzLTRhMjktODgyYi0xYjg0ZWJkMjM5NGQiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6RkM1NjM0NEE5M0VFMTFFNDk1OEFENjBBMUJBQjkyMzkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6RkM1NjM0NDk5M0VFMTFFNDk1OEFENjBBMUJBQjkyMzkiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIChNYWNpbnRvc2gpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MjcyNzhjZDktYmE0ZC00Yjk0LTk2MmYtMzMyZDY3YmJlYWZjIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOmE1OTRhNzNhLTM3MTMtNGEyOS04ODJiLTFiODRlYmQyMzk0ZCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PvEBREYAAA+ZSURBVHja7J15VJTVG8cfNgVBVkVxRVEUNwShlOMSYKmp7SpqZam58oea+1L98phLmVm5FWQd0zA7HcvtuBtoubCKGyiKJq6BLIIgCL/3eWFwVmZGYOadme+H8xzmHe673DvvfLn3vs/zXCvaRbrSULBBgoULFihYB8FcBHMgoEpW1e+WaAoANPBIsDzBrgiWKNhhwfYLVqLLzlY6iBd//WYL9n6VWAGIFwD1BYvZZsG+kPsWqcW6hr/ZCrZAsMuCzYBwAQAMgEuV3rDuLKzSIb3Ey0uwI4J9hmEhAMAIsO4sE+xolR7pJF4+gv0tWD+0HwDAyPSt0iMfbeLFMzQHBfNGmwEAJIJ3lS610iRePLaMEawd2goAIDFYl34huTkwefGaU9VFAwAAqQ4h58g2ZK4SLahydr8R2qeOgKsEAPVBkWAdBbtlLdfrgnABAKROI1nvi8XLXrD30CYAABOB9cqexYtDflzRHgAAE4H1ahCLVzjaAgBgYoSzeAWgHQAAJkYgi1dHtAMAwMTowA5fzlK5GhdbFwpyDSJ/Z39q16gdeTt4i789GnhQY9vG5GjjKJYrfFJIBWUFlP04m64VXaPMR5ni75T8FIrPjae8sjx8tACYNy7s51VhrLPbWNlQb7feNNRzqGjdGncjayvrWh2zvKKczhWcoz339tDuu7vpVO4pelLxxPCVg58XAPWKUcTL19GXxrcZT++3ep88G3rW67nultylH2/+SNE3ouly4WWIFwAQL/3p696XFndcTC81fUk4sZVBK1oh/By4f4CWXl5KJ3JOQLwAgHhpJ8AlgD73+5zCm0jDK+PQf4dozoU5lJyfDPECwESxrs+D8wT82q5r6XTf05IRLmZgk4F0pt8Z+qrrV+I1AgDQ86qGJ+JjAmOorUNbSTdAZlEmjU4aTScfnETPCwBL73nN8ZlDcSFxkhcuxruRN8WGxNJsn9m4GwCwVPFi14cN3TfQKr9VZGtlazKNYGdlJ87Jre++XqwDAMCCxKuBdQPa0WsHTWk7xWQbY2rbqbQ9cLtYFwCABYgX91a2BWyj15u/bvIN8qbXm7Q1YCt6YABYgnjxkIu/9ObCW15viUNfAIAZi9erzV+lGe1nmF3DzGw/k15p9gruEADMUbxaO7Smzf6bDe4tbwi4Tpt7bhbrCAAwM/Fa3WU1udm5mW3juNu5i3UEAJiReIV6hNIIrxFm30BcR64rAMBMxGul30qLaaTlfstxpwBgDuL1gscLFOwabDGN9Lzr82KdAQDS4Znc4Me3Hq9TOU4C+MO/P4gZT6d7TxezodbEwfsHKTYnlt5t9S51dKzMTs2pbL6/8T3lPM6hSW0nifNQ6uAYxeh/o6mPWx962fPl6vd33tkpZpEoLS9V2YedUYc2G0qDmw7Wqc7Hso/hjtGTCLcIWtB5gWJP9tJyinkQYxH1T+mTYrF1l5x48Rf+lea6uRCwmEw+O1l8faXoCkX1iNJYNr0wnYacHiIK3tasrXQ17Kr4/k///lR9jH339tGRPkfUOpAOOzOMzhecF58SJvZPpJ7OPcVg69fja3ac3XB9A6UOSCU/J78ayw1vNlwMIyqtKMVdowcedh7Uw6OHynuWgiXXXXLDRp681jWNDOeUl5H2MK3GspzlVJaumfPRy/LQpxU+3Y97ZZ9e/lTt/ixcsp7ahYIL4mtd8nXxOR+UPtBaztXOlUKbYOIeAJPtefGwTFcqKuo+286yy8tEAdVlDqpCLtsP99a4NyYPv8e580PcQnSuO2djBQCYoHgpC4Ch4Z7S2KSxlNI/hZo0aKLzfk42ThTfL75W5zZ23YHpYbXbCo0gFfHq0riL0S/6VvEtei/5Pdr13C6DevdrmxcDhoUfBgS7BJNLg6fTGEm5SbTu3jq9jrOk5RJq61iZey7vcR7tub+HjhQeId8GvvSi64sKZfU99nTP6QrbB3MPUvrj9OrtMMcw8nN8el9dLLwonlu2b4Dr0zWht2Vtq/4beAbxkopHPS9ttubqGprVfpZuPTbhJyEvQeE9a+Gns1NncrBxMKm6WzosNpGdI8nTQf3KUytLV1LMtRiamD5R63HmdZtHjnaOCu/PEn6+PPclXS26St8+962ieO3WT7yU9488HUnp956K15iWY2iC74Tq7ej0aPK870lrA9eq1I/Lnc0+SyMSRigIIMRLR3ji2lhwz4cF5O8Hf4vbCy4toP4e/SnIJUjrvg/LHlJQnGo5zqSa2C9RJ2EyZt1BJVG+UQpfdnWwGHGZYI9g8v/HX22Z1d6raVY3zf/4+G/7b+43eP2c7Zwp6rkoFUGVwU8v9/XeRz6xPhZ/L+j9tNGYQdicnXVb4LZqoXlc/pgiEiIovyz/mY/J/mHKPTKNjWVlDfUwco9Lm3Apf9F/7fqryvs8VJvcabLW/Qe1GmTwOo5oN0KjcMlo79xeFF+Il57IXBiMBefFj/aPrt7OKMqgKanPnr21a+Ouoge9LhSUFUBBjATPP/EQT57C0kL6KOkjcVKcbfSJ0XQ1/6qKGCjPO83tOFdFIHi41ulAJ/E4PLRTPo4hUa4XX5vKfevaFeKl7w73S+4b/aI5Y+s072nV279k/aJ1H/buzwjLULBrYdcouX+yVs9/GXdK7kBFjMTkFpNVBGfi6Ym0NGtp9TZ7rg85OYTuPbqnUG54i+E19qhYHHh+TDaPxJPyfBwWEWMwL2meQr342niuSx4vBy+Il747yDuNGhNOVePv7K9HRa2pfaP2CsbzXfosFMKOtMA49G7SW2Gb56PUhdmwAP2c8bPCe32b9a1+rdwLY1ZlrlJ7nL039xql16XuieaZ7DO4CWorXqn5qZK4cHtre3FdyEY2jQx2zuS8ZNwxRsLfQ/Ef1fnc8xrLsquDPNxjY7cKRt71gOHhoaYnd6m5hr/XM/Iz8GHriN5PGzk4eVHHRXqfKD43nnyOKD4hsbexp0jvSHHVnmeB3Ry+7vo1TTw7UWvZgicFKudnD/thzYaJvThdHkQcyYaPjbFQHjKyG4PGz0mNL5SmmMKHpQ81HienNAcNb07iFZcTR4VPCsnRxlFrWSurp4JQXF6s9oaLPBdJo1qMUt1Xx6eaE9pMoMPZh9XOe1nLdSzLK8rVnp99xV5r/hr1d+9f43n4Rq7zVbUBAIYbNpaUl9Cuu7t0Ksvez9rg/4g89GMfLs7awPg6+pKzrXPlcEFuXquXay+1x9jYfWN1Ch3uTXV37i6+DnIN0iqCfE6vhtonP2OyYsS6A+OgPHnOc5aaYFcIZbJLs9WW9XHW7C+lPMQEJt7zYjZd30QRLSK0lhvXepzovc7ZHdQFaTvaOtJIr5Hi/BXfjLEhsWLPTv7Y3CtjgbldcltjHjEWuqN9jtL2W9sp0CWQujeuFK9eLr3oUO9D4nCvrLxMVbis7cTcXzLh0wQHeH934zvcLUYkJTuFQpo/DaCvyVVgaNOhKsInm9zn8CHl4ShP4qubJGcnV2Bm4vVX9l90JveM1myq3Oth8VE3LFRHb7feoikfQ5c1IVvat1QbKhTWJEy02sA9Tfn0PsDwnPzvpIJ4sbtDxPUIlSeO7A/2ts/bCu8dv3u8+jWLFIcPyc+hzeo8SyXmkJ1AlXNxATMQL+6JLEpbRAeeN//0MGUVZbQkbQnulDqExWKSzySdysrCezbd2iR6xcuLDofRBKcF04eZH4rb/ERxWfdlKjGBu24pTnNw3KO8pz57rCeGJoquEfml+WKPC8JlpuLFcMrmvff2KqRcNke+ufYNnc0/izulDmGx0BfuFa08t5I+DfhUYcjHMYg1xSjuuLZDZUjIfl2hzUMVroOPxd74ysNNbaE6wHjUKliP0zObc8gMO6V+nP4x7hKJwF7n+gRLsw/X4suL1QrhotRFNYYAsXBtStuERjdX8bpZfJOmpU4zy4bhoO8xiWMQzygxBicPFuP+lEOAlIWHQ34484ImB1RZKBGXkxcxPi4LZODRwBp9yYDxsaJdVOtczWu6rqEZ7WaYVcNMTZ1KG69vfPYDZFX9bombrL6oq2SEmlCXfgeZUc1MvNi3akevHWLAtDmw4soKMVdYrYB4SRbl5cg4blBd4kIuJz9xz8HRmvKDAcNjWxcH4bzyEYkRtDNoJw3xHGLSDcLLri28tBB3hhnjZOekMFnPjqqc/ln21JKdXDltjvITx7T8NDSeufW8ZPCajrw24zut3jHJxuDU0m/EvyHOd9Ua9Lwki7YsqpoIPxqOHPISok5Tg/KXflzyOPok/RMxltCU+OPOH3UnXEDScA9L3xTPnNMewmXG4sWwA+v/0v9HA08OFFf5MQW23NwiLmoA4bIc+KklC1JNTy0ZnufizKqyISUw02GjMu527rTcbzlNbD1RsvnfV2WsovkX5yssUFsnYNhoMvBTy4FNByq8d73wOp3IPYHelqWKlwyOV1zReQUN8BggmYqXVpSKPmpRN6Lq5wQQLwBMX7xkhDcJp/kd5ou/jbkKEeeiH5UwimJzYuvvJBAvAMxHvGR0cupEU9pOodEtRlOzhs0Mem5e83FkwkjKKs6q3xNBvAAwP/GSwc6t/dz70WDPwTTAfYCYPFCfBTH0ZX3meppxfoY4ZKx3IF4AmK94KeNk60Q9nXuKayl2a9xNTM3cw7n2qUlyS3Ppg7Mf0G+3fzNcZSBeAFiOeKkjxC2EtgRsqTHtb00czzlOY5PG0o1HNwx74RAvAOoVya9fz3NUiy7pv1oRJxFkZ9nQf0INL1wAgHrH1hQuklPv6MOFgguip398Xjw+YQDQ8zIevIiHLnCA+MqMlRQYFwjhAgA9L+PTxqGN1jK8QAZPyvPCIAAAy+h5PZL6RXZx6qLxb0VPimjuxbkUFBcE4QLAcijmnlc+j8ykfJW8IK06fr/zO808PxMT8gBYHnksXpcFayblq+zg2EFhOyEvgWZfmE3Hso/hIwTAMrnC4sVLCPeV8lWeyj0lznvFZsfSuuvr6M87f9Z9FggAgCmRxE6qrwovdqIt6hg4qQJQn7zGE/acUjIXbQEAMBFYr/azeBUL9iPaAwBgIrBeFcucVD8XrAhtAgCQOKxTX/ALmXhxsvllaBcAgMRhncqSFy9mlWDH0TYAAIlyvEqnSFm8ygQbLVgm2ggAIDEyq/SpTJ14MZy+YSAEDAAgMeEaWKVPpEm8mAzBQgSLQ5sBACQwVAyp0iXSJl7MbcHCBFtIJhC4DQAwO1h3OAtpaJUeka7iRVVjy+WCdRTsK8Hy0J4AgHomr0pvWHc+I7k5LmU4PEhX7AUbJFi4YIGCcbS0q2AN0d5qQHgQANoooUpv+SuCJQp2mCojfop12fn/AgwAMrwoSkCvPzAAAAAASUVORK5CYII=">
							</button>
						</form>
					</section>
				__HTML__
				push @section,$parts;
			}
			
			if(!($ENV{'HTTP_USER_AGENT'} =~ /mobile/sig)){
				my $section = <<"				__HTML__";
					<section>
						<h2>この画面にスマートフォンからアクセスする</h2>
						<img src="https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=${href}">
					</section>
				__HTML__
				push @section,$section;
			}
			
			my $section = <<"			__HTML__";
				<section>
					<form method="post" onsubmit="return confirm('キャンセルしてもよろしいですか？')">
						<input type="hidden" name="method" value="remove">
						<input type="hidden" name="token" value="$_GET{'token'}">
						<div class="button">
							<button>キャンセル</button>
						</div>
					</form>
				</section>
			__HTML__
			push @section,$section;
			
		}
		else {
			my $section = <<"			__HTML__";
				<section>
					<p>この整理番号は使用済み、あるいは取り消されました</p>
				</section>
			__HTML__
			push @section,$section;
		}
		if($ENV{'HTTP_REFERER'}){
			$_HTML{'footer'} = '<footer><p><a href="' . $ENV{'HTTP_REFERER'} . '">Webサイトに戻る &gt;</a></p></footer>';
		}
	}
	else {
		## Wait screen
		my ($num,$code,$hash,$time,$waitTime,$value) = split(/\t/,$numticket[0]);
		my $qty = @numticket;
		my $min = &_MIN(($config[1]*60)*($qty+1));
		my $section = <<"		__HTML__";
			<section class="ticket" id="html_next_wrapper">
				<p>次の整理番号<strong id="html_next">${num}</strong></p>
			</section>
			<section class="ticket">
				<p>現在の待ち時間<strong id="html_total_waitTime">${min}</strong></p>
				<p class="center">（<span id="html_total_index">${qty}</span>人が待っています）</p>
			</section>
		__HTML__
		push @section,$section;
	}
}
if($redirect){
	print "Location: ${redirect}\n\n";
}
elsif($jsonp){
	print "Pragma: no-cache\n";
	print "Cache-Control: no-cache\n";
	print "Content-type: javascript/json; charset=UTF-8\n\n";
	print $jsonp;
}
elsif(!$err){
	if(@result > 0){
		$_HTML{'content'} = join("\n",@result);
	}
	else {
		$_HTML{'content'} = join("\n",@section);
	}
	foreach $key (keys(%_HTML)){
		$html =~ s/_%%$key%%_/$_HTML{$key}/ig;
	}
	$html =~ s/_%%(.*?)%%_//ig;
	print "Pragma: no-cache\n";
	print "Cache-Control: no-cache\n";
	print "Content-type: text/html; charset=UTF-8\n\n";
	print $html;
}
1;