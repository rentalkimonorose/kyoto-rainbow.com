use MIME::Base64;
use Encode;
use LWP::UserAgent;
use HTTP::Request::Common qw(POST);
use HTTP::Request;

my $ua = LWP::UserAgent->new;
$ua->default_header('Authorization' => "Bearer $config{'LineNotify.AccessToken'}");
my $uri = 'https://notify-api.line.me/api/notify';
my %_LINE_POST = ();
$_LINE_POST{'message'} = $_TEXT{'LineNotify.Message'};
my $req  = POST($uri, [%_LINE_POST]);
my $doc = $ua->request($req)->as_string;
1;