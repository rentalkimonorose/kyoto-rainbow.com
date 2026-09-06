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
my @value = ();
my @name = split(/\,/,$config{"file.numticket.value"});
for(my $i=0;$i<@name;$i++){
	if($_POST{$name[$i]}){
		my $value = "\[ ${name[$i]} \] " . &_SANITIZING($_POST{$name[$i]});
		push @value,$value;
	}
}

my @ntconfig = &_DB($config{"file.numticket.config"});
my @numticket = &_DB($config{"file.numticket.list"});
my $waitTime = $ntconfig[1] || 10;
my $qty = @numticket;

my $time = time;
my @data = ($numticket,$passwd,$hash,$time,($waitTime*60*($qty+1)),join("<br />",@value));
my $data = "\n" . join("\t",@data);
push @numticket,$data;
&_ADDSAVE($config{"file.numticket.list"},$data);
my @config = &_DB($config{"file.numticket.config"});
&_NUMTICKET_JSON($config[1],$config[2],@numticket);
## Token create
my @token = ($numticket,$passwd,$time);
&_SAVE("$config{'dir.numticket.token'}${hash}.cgi",join("\n",@token));
my $uri = &_MFP2URI("module=numticket&token=${hash}");
$config{'ThanksPage'} = $uri;

$_POST{'mfp_numticket_uri'} = $uri;
$_POST{'mfp_numticket_number'} = $numticket;
$_POST{'mfp_numticket_code'} = $passwd;
$_POST{'mfp_numticket_qty'} = ($qty+1);
$_POST{'mfp_numticket_wait'} = ($qty+1) * $ntconfig[1];
my $time = time;
$time += $ntconfig[1] * ($qty+1) * 60;
my ($sec,$min,$hour,$day,$mon,$year) = localtime($time);
$_POST{'mfp_numticket_datetime'} = sprintf("%02d:%02d",$hour,$min);

1;