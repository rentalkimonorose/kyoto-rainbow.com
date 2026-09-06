## 京
use LWP::UserAgent;
use HTTP::Request::Common qw(POST);

my %_GSC = ();
$_GSC{'SPREADSHEET_ID'} = $config{'gsc.id'};
$_GSC{'SHEET_NAME'} = $config{'gsc.name'};

foreach $key ( keys( %_POST ) ) {
	my $val = &_SANITIZING($_POST{$key});
	$_GSC{$key} = $val;
}
foreach $key ( keys( %_ENV ) ) {
	my $val = &_SANITIZING($_ENV{$key});
	$_GSC{$key} = $val;
}
foreach $key ( keys( %_GSC ) ) {
	$_GSC{$key} =~ s/&#x2c;/\,/ig;
}
my $request = POST( $config{'gsc.action'}, [%_GSC] );
my $ua = LWP::UserAgent->new;
my $res = $ua->request($request);
1;