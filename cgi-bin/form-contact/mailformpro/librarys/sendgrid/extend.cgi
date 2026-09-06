sub _SENDMAIL {
	my($to,$from,$name,$subject,$body,$attached,$htmlmail) = @_;
	use LWP::UserAgent;
	use HTTP::Request::Common qw(POST);
	my $ua = LWP::UserAgent->new;
	$ua->default_header('Authorization' => "Bearer $config{'sendgrid.apikey'}");
	$ua->default_header('Content-Type' => "application/json");
	my $url = $config{'sendgrid.uri'};
	$subject = &_JSON($subject);
	$body = &_JSON($body);
my $json = <<__POST_JSON__;
{
  "personalizations": [
    {
      "to": [
        {
          "email": "${to}"
        }
      ],
      "subject": "${subject}"
    }
  ],
  "from": {
    "name": "$config{'sendgrid.name'}",
    "email": "$config{'sendgrid.from'}"
  },
  "content": [
    {
      "type": "text/plain",
      "value": "${body}"
    }
  ]
}
__POST_JSON__
	my $req= HTTP::Request->new(POST => $url);
	$req->content($json);
	my $callback = $ua->request($req)->as_string;
	#print $ua->request($req)->as_string;
	#&_SAVE("json.txt",$json);
	#&_SAVE("callback.txt",$ua->request($req)->as_string);
}
sub _JSON {
	my($str) = @_;
	$str =~ s/\"/&quot;/ig;
	$str =~ s/\\/\\\\/ig;
	$str =~ s/\r//ig;
	$str =~ s/\n/\\r\\n/ig;
	return $str;
}
1;